"""Orchestrator service for coordinating agent workflows."""

from typing import TypedDict, Sequence, Literal, Dict, Any, Optional, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm.providers import Message, LLMProvider
from app.tools.execution import parse_tool_calls
from app.tools.registry import get_tool_registry
from app.utils.helpers import clean_response, find_demo_match, load_demo_prompts
from app.core.config import settings


# Agent state
class AgentState(TypedDict):
    """State for the agent workflow."""
    messages: Sequence[BaseMessage]
    tool_calls: list
    animation_steps: list  # Track animation steps for visualization
    diagram_nodes: list    # Track nodes for diagram
    diagram_edges: list    # Track edges for diagram


class OrchestratorService:
    """Orchestrator service for coordinating specialized agents."""
    
    # Tool icon mapping
    TOOL_ICONS = {
        "scan_ports": "📡",
        "check_service_status": "🔍",
        "analyze_logs": "📋",
        "deploy_config": "🚀",
        "security_scan": "🛡️",
        "check_headers": "📋",
        "test_https": "🔒",
        "analyze_login_form": "📝",
        "check_session_security": "🍪",
        "test_rate_limiting": "🚦",
        "check_password_policy": "🔐",
        "execute_command": "⚙️",
        "check_vulnerability": "⚠️",
        "test_api_security": "🔧",
    }
    
    # Background colors for steps
    BG_COLORS = ["#e8f5e8", "#f3e5f5", "#e3f2fd", "#fff3e0", "#fce4ec"]
    
    def __init__(self):
        """Initialize the orchestrator service."""
        self.tool_registry = get_tool_registry()
        self.demo_prompts = load_demo_prompts()
        self.workflow = self._create_workflow()
        self.llm_provider = None  # Will be set per request
        logger.info("Orchestrator service initialized (database-aware)")

    
    def _should_continue(self, state: AgentState) -> Literal["tools", "end"]:
        """
        Decide whether to use tools or end.
        
        Args:
            state: Current agent state
            
        Returns:
            Next step: "tools" or "end"
        """
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage):
            tool_calls = parse_tool_calls(last_message.content)
            if tool_calls:
                return "tools"
        return "end"
    
    def _call_model(self, state: AgentState) -> Dict[str, Any]:
        """
        Call the LLM.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with LLM response
        """
        messages = state["messages"]

        # Build prompt with tool information
        if len(messages) == 1 or not any("TOOL_RESULT" in str(m.content) for m in messages):
            # Create a custom tool prompt that includes our tools
            tool_definitions = self.tool_registry.get_tool_definitions()
            
            tool_prompt = f"You have access to the following tools:\n{tool_definitions}"
            tool_prompt += "\n\n⚠️ CRITICAL INSTRUCTIONS:"
            tool_prompt += "\n1. You MUST use tools to perform actual security scans - NEVER make up or hallucinate results"
            tool_prompt += "\n2. For port scanning, network analysis, or any technical task, you MUST call the appropriate tool"
            tool_prompt += "\n3. To use a tool, respond ONLY with: TOOL: tool_name(param1=value1, param2=value2)"
            tool_prompt += "\n4. Do NOT provide an answer without calling tools first"
            tool_prompt += "\n5. Example: For 'scan ports on localhost', respond with: TOOL: scan_network(target=localhost, ports=1-65535)"
            tool_prompt += "\n\nIf you provide results without calling tools, you are HALLUCINATING and providing FALSE information."
            
            system_msg = SystemMessage(
                content=f"You are CMatrix, an advanced AI security orchestrator. "
                f"You coordinate specialized worker agents to perform security assessments.\n\n{tool_prompt}"
            )
            prompt_messages = [system_msg] + list(messages)
        else:
            prompt_messages = messages

        # Convert LangChain BaseMessage objects to provider Message objects
        provider_messages = []
        for msg in prompt_messages:
            if isinstance(msg, SystemMessage):
                provider_messages.append(Message(role="system", content=msg.content))
            elif isinstance(msg, HumanMessage):
                provider_messages.append(Message(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                provider_messages.append(Message(role="assistant", content=msg.content))
            else:
                # Fallback for unknown message types
                provider_messages.append(Message(role="user", content=str(msg.content)))

        # Use provider interface with Message objects
        response = self.llm_provider.invoke(provider_messages)

        # Validate response is not empty
        if not response or not response.strip():
            response = "I apologize, but I couldn't generate a proper response. Please try again."
            logger.warning("LLM returned empty response, using fallback message")

        # Preserve animation/diagram state
        return {
            "messages": [AIMessage(content=response)],
            "animation_steps": state.get("animation_steps", []),
            "diagram_nodes": state.get("diagram_nodes", []),
            "diagram_edges": state.get("diagram_edges", [])
        }
    
    def _call_tools(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute tools and add results to messages.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with tool results
        """
        last_message = state["messages"][-1]
        tool_calls = parse_tool_calls(last_message.content)

        # Get existing animation steps and diagram data
        animation_steps = state.get("animation_steps", [])
        diagram_nodes = state.get("diagram_nodes", [])
        diagram_edges = state.get("diagram_edges", [])

        if tool_calls:
            results = []
            step_number = len(animation_steps) + 1
            
            for idx, (tool_name, tool_args) in enumerate(tool_calls):
                # Generate animation step for this tool
                icon = self.TOOL_ICONS.get(tool_name, "🔧")
                bg_color = self.BG_COLORS[idx % len(self.BG_COLORS)]
                
                animation_step = {
                    "step": step_number + idx,
                    "title": f"Executing {tool_name.replace('_', ' ').title()}",
                    "description": f"Running {tool_name} with parameters: {', '.join(f'{k}={v}' for k, v in tool_args.items())}",
                    "duration": 1500,
                    "icon": icon,
                    "bgColor": bg_color
                }
                animation_steps.append(animation_step)
                
                # Add node to diagram
                node_id = f"tool_{step_number + idx}"
                diagram_nodes.append({
                    "id": node_id,
                    "label": tool_name.replace('_', ' ').title(),
                    "x": 350 + (idx * 150),
                    "y": 50 + (idx % 2) * 40,
                    "type": "tool"
                })
                
                # Add edge from previous node
                if diagram_nodes:
                    prev_node_id = diagram_nodes[-2]["id"] if len(diagram_nodes) > 1 else "ai"
                    diagram_edges.append({
                        "from": prev_node_id,
                        "to": node_id
                    })
                
                # Execute the tool
                if self.tool_registry.tool_exists(tool_name):
                    try:
                        tool_info = self.tool_registry.get_tool(tool_name)
                        func = tool_info["function"]
                        if hasattr(func, "invoke"):
                            result = func.invoke(tool_args)
                        else:
                            result = func(**tool_args)
                        results.append(f"Tool '{tool_name}' output: {result}")
                        logger.info(f"Executed tool '{tool_name}' successfully")
                    except Exception as e:
                        error_msg = f"Error executing '{tool_name}': {str(e)}"
                        results.append(error_msg)
                        logger.error(error_msg, exc_info=True)
                else:
                    error_msg = f"Tool '{tool_name}' not found."
                    results.append(error_msg)
                    logger.warning(error_msg)
            
            results_str = "\n\n".join(results)
            return {
                "messages": [HumanMessage(content=f"TOOL_RESULTS:\n{results_str}\n\nNow provide your final answer based on these results.")],
                "animation_steps": animation_steps,
                "diagram_nodes": diagram_nodes,
                "diagram_edges": diagram_edges
            }

        return {
            "messages": [],
            "animation_steps": animation_steps,
            "diagram_nodes": diagram_nodes,
            "diagram_edges": diagram_edges
        }
    
    def _create_workflow(self):
        """
        Create and configure the orchestrator workflow.
        
        Returns:
            Compiled workflow
        """
        # Build graph
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {"tools": "tools", "end": END}
        )
        workflow.add_edge("tools", "agent")

        return workflow.compile()
    
    async def run(
        self,
        message: str,
        user_id: int,
        db: AsyncSession,
        history: Optional[list] = None,
        is_demo_page: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Run the orchestrator with a message and optional history.
        
        Args:
            message: User message
            user_id: User ID for loading LLM configuration
            db: Database session
            history: Optional conversation history
            is_demo_page: Whether the request is from the demo page
            
        Returns:
            Response string or dict with animation data
        """
        # Check if the message matches any demo prompt using fuzzy matching
        if is_demo_page:
            best_match = find_demo_match(message, self.demo_prompts)
            if best_match:
                demo_data = self.demo_prompts[best_match]
                logger.info(f'DEMO MATCH FOUND - Using default answer, NOT calling LLM')
                return {
                    "animation_steps": demo_data["animation_steps"],
                    "diagram": demo_data.get("diagram"),
                    "final_answer": demo_data["final_answer"]
                }

        # Load user's active LLM provider from database
        from app.services.llm.db_factory import get_db_provider_factory
        factory = get_db_provider_factory()
        llm_provider = await factory.get_active_provider(db, user_id)
        
        if not llm_provider:
            raise ValueError("No active LLM model configured. Please configure an API key and activate a model in settings.")
        
        # Set the provider for this request
        self.llm_provider = llm_provider
        
        # No demo match found - proceed with LLM processing
        logger.info(f'No demo match found - calling LLM for user {user_id}')
        messages = []

        # Add history
        if history:
            for msg in history:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

        # Add current message
        messages.append(HumanMessage(content=message))

        try:
            # Run agent with animation/diagram tracking
            result = self.workflow.invoke({
                "messages": messages,
                "tool_calls": [],
                "animation_steps": [],
                "diagram_nodes": [],
                "diagram_edges": []
            })

            # Extract final response
            final_message = result["messages"][-1]
            content = final_message.content if hasattr(final_message, 'content') else str(final_message)

            # Clean up the response
            cleaned_content = clean_response(content)

            logger.info(f'Orchestrator response: {cleaned_content[:200]}...' if len(cleaned_content) > 200 else cleaned_content)

            # Check if we have animation steps (tool execution occurred)
            animation_steps = result.get("animation_steps", [])
            diagram_nodes = result.get("diagram_nodes", [])
            diagram_edges = result.get("diagram_edges", [])

            if animation_steps:
                # Add initial nodes for user and AI
                initial_nodes = [
                    {"id": "user", "label": "User Query", "x": 50, "y": 50, "type": "user"},
                    {"id": "ai", "label": "AI Agent", "x": 200, "y": 50, "type": "ai"}
                ]
                
                # Add result node
                result_node = {
                    "id": "result",
                    "label": "Final Answer",
                    "x": 350 + (len(diagram_nodes) * 150),
                    "y": 50,
                    "type": "result"
                }
                
                # Create edges
                initial_edges = [{"from": "user", "to": "ai"}]
                
                # Connect AI to first tool
                if diagram_nodes:
                    initial_edges.append({"from": "ai", "to": diagram_nodes[0]["id"]})
                    # Connect last tool to result
                    diagram_edges.append({"from": diagram_nodes[-1]["id"], "to": "result"})
                
                # Combine all nodes and edges
                all_nodes = initial_nodes + diagram_nodes + [result_node]
                all_edges = initial_edges + diagram_edges
                
                logger.info(f'Generated {len(animation_steps)} animation steps and diagram with {len(all_nodes)} nodes')
                
                return {
                    "animation_steps": animation_steps,
                    "diagram": {"nodes": all_nodes, "edges": all_edges},
                    "final_answer": cleaned_content
                }
            
            # No tools were executed, return regular response
            return cleaned_content

        except Exception as e:
            logger.error(f"Error in orchestrator: {str(e)}", exc_info=True)
            raise


# Global orchestrator instance
_orchestrator_service: Optional[OrchestratorService] = None


def get_orchestrator_service() -> OrchestratorService:
    """
    Get or create global orchestrator service instance.
    
    Returns:
        OrchestratorService instance
    """
    global _orchestrator_service
    if _orchestrator_service is None:
        _orchestrator_service = OrchestratorService()
    return _orchestrator_service


async def run_orchestrator(
    message: str,
    user_id: int,
    db: AsyncSession,
    history: Optional[list] = None,
    is_demo_page: bool = False
) -> Union[str, Dict[str, Any]]:
    """
    Run the orchestrator with a message and optional history.
    
    This is a convenience function that uses the global orchestrator instance.
    
    Args:
        message: User message
        user_id: User ID for loading LLM configuration
        db: Database session
        history: Optional conversation history
        is_demo_page: Whether the request is from the demo page
        
    Returns:
        Response string or dict with animation data
    """
    orchestrator = get_orchestrator_service()
    return await orchestrator.run(message, user_id, db, history, is_demo_page)

