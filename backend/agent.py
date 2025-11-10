import os
import re
from typing import TypedDict, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

from tool_execution import create_tool_prompt, parse_tool_calls, execute_tools
from tools import TOOLS
from llm import HuggingFaceLLM
from utils import DEMO_PROMPTS, clean_response, find_best_matching_demo

# Agent state
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    tool_calls: list

def create_agent():
    """Create and configure the agent workflow."""
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
            tool_prompt = create_tool_prompt()
            system_msg = SystemMessage(content=f"You are DeepHat, created by Kindo.ai. You are a helpful assistant that is an expert in Cybersecurity and DevOps.\n\n{tool_prompt}")
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
            results = execute_tools(tool_calls)
            return {"messages": [HumanMessage(content=f"TOOL_RESULTS:\n{results}\n\nNow provide your final answer based on these results.")]}

        return {"messages": []}

    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()

# Create agent instance
agent_executor = create_agent()

def run_agent(message: str, history: list = None):
    """Run the agent with a message and optional history."""
    # Check if the message matches any demo prompt using fuzzy matching
    best_match, similarity = find_best_matching_demo(message)
    if best_match:
        demo_data = DEMO_PROMPTS[best_match]
        print(f'✅ DEMO MATCH FOUND (similarity: {similarity:.2f}) - Using default answer, NOT calling LLM')
        print(f'Demo prompt: {best_match[:100]}...')
        print(f'Final answer: {demo_data["final_answer"][:100]}...')
        # Return both the animation steps, diagram data, and final answer - LLM is NEVER called for demo matches
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
        result = agent_executor.invoke({"messages": messages, "tool_calls": []})

        # Extract final response
        final_message = result["messages"][-1]
        content = final_message.content if hasattr(final_message, 'content') else str(final_message)

        # Clean up the response
        cleaned_content = clean_response(content)

        print('✅ Agent response:', cleaned_content[:200] + '...' if len(cleaned_content) > 200 else cleaned_content)

        return cleaned_content

    except Exception as e:
        print(f"❌ Error in run_agent: {str(e)}")
        raise
