import os
from typing import TypedDict, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

from tool_execution import create_tool_prompt, parse_tool_calls, execute_tools
from llm import HuggingFaceLLM
from utils import DEMO_PROMPTS, clean_response, find_best_matching_demo

# Import authorization and audit logging
from authorization import auth_manager
from audit_logger import audit_logger

# Import tools from worker agents
from agents.network_agent import NETWORK_TOOLS
from agents.web_agent import WEB_TOOLS
from agents.auth_agent import AUTH_TOOLS
from agents.config_agent import CONFIG_TOOLS
from agents.vuln_intel_agent import VULN_INTEL_TOOLS
from agents.api_security_agent import API_SECURITY_TOOLS
from agents.command_agent import COMMAND_TOOLS

# Aggregate all tools
ALL_TOOLS = {
    tool.name: {
        "description": tool.description,
        "parameters": list(tool.args.keys()),
        "function": tool.func if hasattr(tool, "func") else tool
    }
    for tool in (NETWORK_TOOLS + WEB_TOOLS + AUTH_TOOLS + 
                 CONFIG_TOOLS + VULN_INTEL_TOOLS + API_SECURITY_TOOLS + COMMAND_TOOLS)
}

# Agent state
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    tool_calls: list

def create_orchestrator():
    """Create and configure the orchestrator workflow."""
    api_key = os.getenv("HUGGINGFACE_API_KEY")

    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")

    llm = HuggingFaceLLM(api_key=api_key)

    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Decide whether to use tools or end."""
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage):
            tool_calls = parse_tool_calls(last_message.content)
            if tool_calls:
                return "tools"
        return "end"

    def call_model(state: AgentState):
        """Call the LLM."""
        messages = state["messages"]

        # Build prompt with tool information
        if len(messages) == 1 or not any("TOOL_RESULT" in str(m.content) for m in messages):
            # Create a custom tool prompt that includes our new tools
            tool_definitions = []
            for name, tool_info in ALL_TOOLS.items():
                params = ", ".join(tool_info["parameters"])
                tool_definitions.append(f"- {name}({params}): {tool_info['description']}")
            
            tool_prompt = "You have access to the following tools:\n" + "\n".join(tool_definitions)
            tool_prompt += "\n\nTo use a tool, use the format: TOOL: tool_name(param1=value1, ...)"
            
            system_msg = SystemMessage(content=f"You are CMatrix, an advanced AI security orchestrator. You coordinate specialized worker agents to perform security assessments.\n\n{tool_prompt}")
            prompt_messages = [system_msg] + list(messages)
        else:
            prompt_messages = messages

        # Convert to string prompt for HuggingFace
        prompt_text = "\n".join([f"{m.type}: {m.content}" for m in prompt_messages])
        response = llm.invoke(prompt_text)

        return {"messages": [AIMessage(content=response)]}

    def call_tools(state: AgentState):
        """Execute tools and add results to messages."""
        last_message = state["messages"][-1]
        tool_calls = parse_tool_calls(last_message.content)

        if tool_calls:
            # We need to adapt execute_tools to use our ALL_TOOLS dictionary
            # The original execute_tools imported TOOLS from tools.py
            # Here we'll implement a local execution logic or patch TOOLS
            
            results = []
            for tool_name, tool_args in tool_calls:
                if tool_name in ALL_TOOLS:
                    try:
                        # The function might be a langchain tool or a raw function
                        func = ALL_TOOLS[tool_name]["function"]
                        # Handle both direct function calls and LangChain tool objects
                        if hasattr(func, "invoke"):
                            result = func.invoke(tool_args)
                        else:
                            result = func(**tool_args)
                        results.append(f"Tool '{tool_name}' output: {result}")
                    except Exception as e:
                        results.append(f"Error executing '{tool_name}': {str(e)}")
                else:
                    results.append(f"Tool '{tool_name}' not found.")
            
            results_str = "\n\n".join(results)
            return {"messages": [HumanMessage(content=f"TOOL_RESULTS:\n{results_str}\n\nNow provide your final answer based on these results.")]}

        return {"messages": []}

    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()

# Create orchestrator instance
orchestrator_executor = create_orchestrator()

def run_orchestrator(message: str, history: list = None):
    """Run the orchestrator with a message and optional history."""
    # Check if the message matches any demo prompt using fuzzy matching
    best_match, similarity = find_best_matching_demo(message)
    if best_match:
        demo_data = DEMO_PROMPTS[best_match]
        print(f'✅ DEMO MATCH FOUND (similarity: {similarity:.2f}) - Using default answer, NOT calling LLM')
        return {
            "animation_steps": demo_data["animation_steps"],
            "diagram": demo_data.get("diagram"),
            "final_answer": demo_data["final_answer"]
        }

    # No demo match found - proceed with LLM processing
    print('🤖 No demo match found - calling LLM for response')
    messages = []

    # Add history
    if history:
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # Add current message
    messages.append(HumanMessage(content=message))

    try:
        # Run agent
        result = orchestrator_executor.invoke({"messages": messages, "tool_calls": []})

        # Extract final response
        final_message = result["messages"][-1]
        content = final_message.content if hasattr(final_message, 'content') else str(final_message)

        # Clean up the response
        cleaned_content = clean_response(content)

        print('✅ Orchestrator response:', cleaned_content[:200] + '...' if len(cleaned_content) > 200 else cleaned_content)

        return cleaned_content

    except Exception as e:
        print(f"❌ Error in run_orchestrator: {str(e)}")
        raise
