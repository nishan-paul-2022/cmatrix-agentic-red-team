"""Orchestrator service for coordinating agent workflows."""

from collections.abc import Sequence
from typing import Any, Literal, Optional, TypedDict, Union

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.checkpoint import get_checkpointer
from app.services.llm.providers import Message
from app.services.reasoning.reflection import ReflectionTrigger, get_self_reflection
from app.services.reasoning.rewoo import get_rewoo_planner
from app.services.reasoning.tree_of_thoughts import get_tree_of_thoughts
from app.services.supervisor import get_supervisor_service
from app.tools.execution import parse_tool_calls
from app.tools.registry import get_tool_registry
from app.utils.helpers import clean_response


# Agent state
class AgentState(TypedDict):
    """State for the agent workflow with HITL approval support and agent delegation."""

    messages: Sequence[BaseMessage]
    tool_calls: list
    animation_steps: list  # Track animation steps for visualization
    diagram_nodes: list  # Track nodes for diagram
    diagram_edges: list  # Track edges for diagram
    pending_approval: dict  # Pending approval data for HITL gates
    approval_status: str  # Current approval status: "pending", "approved", "rejected"
    auto_rejected: dict  # Auto-rejection data if tool was auto-rejected
    skip_llm: bool  # Flag to skip LLM after approved tool execution
    agent_delegation: dict  # Agent delegation results from supervisor
    use_agents: bool  # Flag to use specialized agents instead of tools
    reflection_count: int  # Track number of reflection loops
    reflection_results: list  # Store reflection history
    # Advanced Reasoning Patterns (Phase 3.2)
    selected_strategy: dict  # Tree of Thoughts selected strategy
    strategy_evaluation: dict  # Strategy evaluation results
    execution_plan: dict  # ReWOO execution plan
    plan_steps: list  # Individual plan steps
    user_preferences: dict  # User preferences for strategy selection
    reasoning_metrics: dict  # Performance telemetry


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
        self.supervisor = get_supervisor_service()
        self.reflection = None  # Will be initialized with LLM
        self.rewoo = None  # Will be initialized with LLM
        self.tot = None  # Will be initialized with LLM (Tree of Thoughts)
        self.checkpointer = None  # Will be lazily initialized
        self.workflow = self._create_workflow()
        self.llm_provider = None  # Will be set per request
        self.current_user_id = None  # Store current user_id for tool injection
        self.current_conversation_id = None  # Store current conversation_id for tool injection
        logger.info(
            "Orchestrator service initialized with multi-agent supervision, advanced reasoning, and checkpointing"
        )

    def _should_continue(
        self, state: AgentState
    ) -> Literal["delegate", "tools", "approval_gate", "end"]:
        """
        Decide whether to delegate to agents, use tools, request approval, or end.

        This method implements intelligent routing:
        1. Check if specialized agents should handle the task (agent delegation)
        2. Check if tools need approval (HITL approval gates)
        3. Execute tools directly
        4. End if no action needed

        Args:
            state: Current agent state

        Returns:
            Next step: "delegate", "tools", "approval_gate", or "end"
        """
        from datetime import datetime

        from app.core.approval_config import (
            check_auto_reject,
            get_tool_risk_info,
            requires_approval,
        )

        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage):
            tool_calls = parse_tool_calls(last_message.content)
            if tool_calls:
                # Check if any tool requires approval
                for tool_name, tool_args in tool_calls:
                    # First check for auto-reject patterns
                    auto_reject_reason = check_auto_reject(tool_name, tool_args)
                    if auto_reject_reason:
                        # Store auto-rejection info
                        state["auto_rejected"] = {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "reason": auto_reject_reason,
                            "timestamp": datetime.now().isoformat(),
                        }
                        logger.warning(f"Tool '{tool_name}' auto-rejected: {auto_reject_reason}")
                        return "end"  # Skip to end with rejection message

                    # Check if approval is required
                    if requires_approval(tool_name, tool_args):
                        risk_info = get_tool_risk_info(tool_name)

                        # Store pending approval in state
                        state["pending_approval"] = {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "risk_info": risk_info.to_dict(),
                            "timestamp": datetime.now().isoformat(),
                            "all_tool_calls": tool_calls,  # Store all calls for later execution
                        }

                        logger.info(
                            f"⏸️ Tool '{tool_name}' requires approval - routing to approval gate"
                        )
                        return "approval_gate"  # Pause for approval

                # No approval needed, proceed with execution
                return "tools"

        # No tool calls - check if we should delegate to specialized agents
        # This happens when the LLM doesn't call tools but the task matches agent expertise
        messages = state.get("messages", [])
        if messages:
            # Get the original user message
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    user_message = msg.content
                    # Quick check if agents should handle this
                    analysis = self.supervisor.analyze_task(user_message)
                    if analysis["primary_agent"] and analysis["confidence"] >= 0.4:
                        logger.info(
                            f"🎯 No tools called, but delegating to agents (confidence: {analysis['confidence']:.2f})"
                        )
                        return "delegate"
                    break

        return "end"

    def _call_model(self, state: AgentState) -> dict[str, Any]:
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
            tool_prompt += "\n1. You MUST use tools to perform actual technical tasks - NEVER make up or hallucinate results"
            tool_prompt += "\n2. For any technical task (scanning, analysis, execution), you MUST call the appropriate tool"
            tool_prompt += "\n3. To use a tool, respond ONLY with: TOOL: tool_name(param1=value1, param2=value2)"
            tool_prompt += (
                "\n4. Do NOT provide an answer for technical queries without calling tools first"
            )
            tool_prompt += "\n5. Example: For 'scan ports on localhost', respond with: TOOL: scan_network(target=localhost, ports=1-65535)"
            tool_prompt += "\n\nIf you provide technical results without calling tools, you are HALLUCINATING and providing FALSE information."

            system_msg = SystemMessage(
                content=f"You are CMatrix, an advanced AI intelligent orchestrator. "
                f"You coordinate specialized worker agents to perform complex tasks.\n\n"
                f"You have access to a Long-Term Knowledge Base. "
                f"ALWAYS check the knowledge base first using 'search_knowledge_base' if the user asks about past conversations, saved facts, or findings. "
                f"When you find important information (like user preferences, personal details, or technical findings), save it using 'save_to_knowledge_base'.\n\n"
                f"{tool_prompt}"
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
            "diagram_edges": state.get("diagram_edges", []),
        }

    def _call_tools(self, state: AgentState) -> dict[str, Any]:
        """
        Execute tools and add results to messages.

        Args:
            state: Current agent state

        Returns:
            Updated state with tool results
        """
        # Check if we're resuming from an approval
        approval_status = state.get("approval_status", "")
        pending_approval = state.get("pending_approval", {})
        is_approved_execution = False

        # If approved, get tool calls from pending_approval
        if approval_status == "approved" and pending_approval:
            tool_calls = pending_approval.get("all_tool_calls", [])
            is_approved_execution = True
            logger.info(f"Resuming approved tool execution: {len(tool_calls)} tool(s)")
        else:
            # Normal flow: get tool calls from last message
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
                    "bgColor": bg_color,
                }
                animation_steps.append(animation_step)

                # Add node to diagram
                node_id = f"tool_{step_number + idx}"
                diagram_nodes.append(
                    {
                        "id": node_id,
                        "label": tool_name.replace("_", " ").title(),
                        "x": 350 + (idx * 150),
                        "y": 50 + (idx % 2) * 40,
                        "type": "tool",
                    }
                )

                # Add edge from previous node
                if diagram_nodes:
                    prev_node_id = diagram_nodes[-2]["id"] if len(diagram_nodes) > 1 else "ai"
                    diagram_edges.append({"from": prev_node_id, "to": node_id})

                # Execute the tool
                if self.tool_registry.tool_exists(tool_name):
                    try:
                        tool_info = self.tool_registry.get_tool(tool_name)
                        func = tool_info["function"]

                        # Auto-inject user_id and conversation_id for memory tools
                        if tool_name in ["search_knowledge_base", "save_to_knowledge_base"]:
                            if self.current_user_id is not None:
                                tool_args["user_id"] = self.current_user_id
                            if (
                                self.current_conversation_id is not None
                                and tool_name == "save_to_knowledge_base"
                            ):
                                tool_args["conversation_id"] = self.current_conversation_id
                            logger.debug(
                                f"Auto-injected context for {tool_name}: user_id={self.current_user_id}, conversation_id={self.current_conversation_id}"
                            )

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

            # If this was an approved execution, skip the LLM and return raw results
            if is_approved_execution:
                return {
                    "messages": [AIMessage(content=results_str)],
                    "animation_steps": animation_steps,
                    "diagram_nodes": diagram_nodes,
                    "diagram_edges": diagram_edges,
                    "approval_status": "",  # Clear approval status after execution
                    "pending_approval": {},  # Clear pending approval
                    "skip_llm": True,  # Flag to skip LLM and go to END
                }
            else:
                # Normal flow: send results back to LLM for interpretation
                return {
                    "messages": [
                        HumanMessage(
                            content=f"TOOL_RESULTS:\n{results_str}\n\nNow provide your final answer based on these results."
                        )
                    ],
                    "animation_steps": animation_steps,
                    "diagram_nodes": diagram_nodes,
                    "diagram_edges": diagram_edges,
                    "approval_status": "",  # Clear approval status after execution
                    "pending_approval": {},  # Clear pending approval
                }

        return {
            "messages": [],
            "animation_steps": animation_steps,
            "diagram_nodes": diagram_nodes,
            "diagram_edges": diagram_edges,
        }

    def _detect_scan_type(self, tool_name: str) -> str:
        """Detect scan type from tool name."""
        tool_lower = tool_name.lower()
        if "port" in tool_lower or "network" in tool_lower or "scan_network" in tool_lower:
            return "port_scan"
        elif "web" in tool_lower or "http" in tool_lower or "header" in tool_lower:
            return "web_scan"
        elif "cve" in tool_lower or "vuln" in tool_lower or "vulnerability" in tool_lower:
            return "cve_search"
        elif "auth" in tool_lower or "login" in tool_lower or "session" in tool_lower:
            return "auth_scan"
        elif "api" in tool_lower:
            return "api_scan"
        else:
            return "general"

    def _extract_target(self, tool_args: dict) -> str:
        """Extract target from tool arguments."""
        # Common parameter names for targets
        for key in ["target", "url", "host", "ip", "domain", "endpoint"]:
            if key in tool_args:
                return str(tool_args[key])
        return "N/A"

    def _assess_severity(self, result: str) -> str:
        """Assess severity from result content."""
        result_lower = result.lower()

        # High severity indicators
        if any(
            word in result_lower
            for word in [
                "critical",
                "high",
                "exploit",
                "vulnerable",
                "exposed",
                "backdoor",
                "malware",
                "breach",
                "compromised",
            ]
        ):
            return "high"

        # Medium severity indicators
        elif any(
            word in result_lower
            for word in [
                "medium",
                "warning",
                "misconfiguration",
                "weak",
                "deprecated",
                "outdated",
                "insecure",
            ]
        ):
            return "medium"

        # Default to low
        else:
            return "low"

    def _extract_tags(self, result: str, tool_name: str) -> list:
        """Extract relevant tags from result and tool name."""
        tags = []
        result_lower = result.lower()

        # Common security tags
        tag_keywords = {
            "ssh": ["ssh", "port 22", "openssh"],
            "http": ["http", "port 80", "apache", "nginx"],
            "https": ["https", "port 443", "ssl", "tls"],
            "mysql": ["mysql", "port 3306", "mariadb"],
            "postgresql": ["postgres", "port 5432"],
            "redis": ["redis", "port 6379"],
            "mongodb": ["mongo", "port 27017"],
            "ftp": ["ftp", "port 21"],
            "smtp": ["smtp", "port 25", "port 587"],
            "dns": ["dns", "port 53"],
            "open-ports": ["open port", "listening", "accessible"],
            "vulnerability": ["cve-", "vulnerability", "exploit", "vulnerable"],
            "misconfiguration": ["misconfigured", "weak", "insecure"],
            "authentication": ["auth", "login", "password", "session"],
            "encryption": ["ssl", "tls", "https", "encrypted"],
        }

        for tag, keywords in tag_keywords.items():
            if any(kw in result_lower for kw in keywords):
                tags.append(tag)

        # Add tool-based tag
        if "scan" in tool_name:
            tags.append("scan")
        if "check" in tool_name:
            tags.append("check")

        return tags[:5]  # Limit to 5 tags

    def _approval_gate(self, state: AgentState) -> dict[str, Any]:
        """
        Approval gate node - pauses execution until user approval.

        This node implements HITL (Human-in-the-Loop) approval gates.
        When a dangerous tool is detected, the workflow pauses here and
        waits for user approval via the API.

        The workflow state is persisted via checkpointing, allowing the
        workflow to resume after approval/rejection.

        Args:
            state: Current agent state with pending_approval data

        Returns:
            Updated state with approval status
        """
        from datetime import datetime

        from app.core.approval_config import get_tool_risk_info, requires_approval

        # Re-calculate pending approval data since conditional edges can't modify state
        pending = {}
        messages = state.get("messages", [])
        if not messages:
            logger.warning("No messages found in state at approval gate")
            return {
                "messages": [AIMessage(content="Error: No messages found for approval context")],
                "approval_status": "error",
            }

        last_message = messages[-1]

        if isinstance(last_message, AIMessage):
            tool_calls = parse_tool_calls(last_message.content)
            if tool_calls:
                for tool_name, tool_args in tool_calls:
                    if requires_approval(tool_name, tool_args):
                        risk_info = get_tool_risk_info(tool_name)
                        pending = {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "risk_info": risk_info.to_dict(),
                            "timestamp": datetime.now().isoformat(),
                            "all_tool_calls": tool_calls,
                        }
                        break

        tool_name = pending.get("tool_name", "unknown")
        risk_info = pending.get("risk_info", {})

        logger.info(f"⏸️ Workflow paused at approval gate for tool: {tool_name}")
        logger.info(f"   Risk level: {risk_info.get('risk_level', 'UNKNOWN')}")
        logger.info(f"   Reason: {risk_info.get('reason', 'N/A')}")

        # Create approval message for user
        approval_message = (
            f"⏸️ **Approval Required**\n\n"
            f"**Tool**: `{tool_name}`\n"
            f"**Risk Level**: {risk_info.get('risk_level', 'UNKNOWN')}\n"
            f"**Reason**: {risk_info.get('reason', 'N/A')}\n\n"
        )

        if risk_info.get("warning"):
            approval_message += f"{risk_info['warning']}\n\n"

        approval_message += (
            "This operation requires your approval before execution. "
            "Please review the details and approve or reject this action."
        )

        # Return state with approval message AND the pending_approval data
        # This ensures the data is persisted in the checkpoint
        return {
            "messages": [AIMessage(content=approval_message)],
            "approval_status": "pending",
            "pending_approval": pending,  # Persist the calculated data
            "animation_steps": state.get("animation_steps", []),
            "diagram_nodes": state.get("diagram_nodes", []),
            "diagram_edges": state.get("diagram_edges", []),
        }

    def _check_approval(self, state: AgentState) -> Literal["approved", "rejected"]:
        """Check approval status to determine next step."""
        status = state.get("approval_status", "pending")
        if status == "approved":
            return "approved"
        return "rejected"

    def _should_delegate_to_agents(self, state: AgentState) -> Literal["delegate", "tools"]:
        """
        Decide whether to delegate to specialized agents or use tools directly.

        This method analyzes the user's message to determine if specialized
        agents should handle the task instead of the general tool execution.

        Args:
            state: Current agent state

        Returns:
            Next step: "delegate" or "tools"
        """
        messages = state.get("messages", [])
        if not messages:
            return "tools"

        # Get the original user message (first HumanMessage)
        user_message = None
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_message = msg.content
                break

        if not user_message:
            return "tools"

        # Quick analysis to see if agents should handle this
        analysis = self.supervisor.analyze_task(user_message)

        # If confidence is high enough and we have a primary agent, delegate
        if analysis["primary_agent"] and analysis["confidence"] >= 0.3:
            logger.info(
                f"🎯 Delegating to specialized agents (confidence: {analysis['confidence']:.2f})"
            )
            return "delegate"

        # Otherwise use tools
        logger.info("Using general tool execution (no strong agent match)")
        return "tools"

    async def _delegate_to_agents(self, state: AgentState) -> dict[str, Any]:
        """
        Delegate task to specialized agent subgraphs via supervisor.

        This node uses the supervisor service to intelligently route tasks
        to the most appropriate specialized agents, aggregate their results,
        and return a synthesized response.

        Args:
            state: Current agent state

        Returns:
            Updated state with agent delegation results
        """
        messages = state.get("messages", [])

        # Extract user message
        user_message = None
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_message = msg.content
                break

        if not user_message:
            return {
                "messages": [AIMessage(content="Error: No user message found for delegation")],
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        logger.info(f"🤖 Delegating to specialized agents: {user_message[:100]}...")

        # Build context from conversation history
        context = {
            "conversation_history": [
                {
                    "role": "user" if isinstance(m, HumanMessage) else "assistant",
                    "content": m.content,
                }
                for m in messages[:-1]  # Exclude current message
            ]
        }

        try:
            # Delegate to supervisor (this is async)
            delegation_result = await self.supervisor.supervise(
                task=user_message, context=context, llm_provider=self.llm_provider
            )

            # Check if delegation occurred
            if delegation_result.get("status") == "no_delegation":
                # No agents matched - fall back to tools
                logger.info("No agent delegation - falling back to tool execution")
                return {
                    "messages": [],  # Empty to continue to tools
                    "use_agents": False,
                    "animation_steps": state.get("animation_steps", []),
                    "diagram_nodes": state.get("diagram_nodes", []),
                    "diagram_edges": state.get("diagram_edges", []),
                }

            # Extract final answer from delegation
            final_answer = delegation_result.get("final_answer", "")
            execution_summary = delegation_result.get("execution_summary", {})

            # Create animation steps for agent execution
            animation_steps = state.get("animation_steps", []).copy()
            diagram_nodes = state.get("diagram_nodes", []).copy()
            diagram_edges = state.get("diagram_edges", []).copy()

            agents_used = execution_summary.get("agents_used", [])
            for idx, agent_type in enumerate(agents_used):
                agent_name = agent_type.replace("_", " ").title()
                icon = "🤖"
                bg_color = self.BG_COLORS[idx % len(self.BG_COLORS)]

                animation_step = {
                    "step": len(animation_steps) + 1,
                    "title": f"Consulting {agent_name}",
                    "description": f"Specialized {agent_name} analyzing the task",
                    "duration": 2000,
                    "icon": icon,
                    "bgColor": bg_color,
                }
                animation_steps.append(animation_step)

                # Add node to diagram
                node_id = f"agent_{agent_type}"
                diagram_nodes.append(
                    {
                        "id": node_id,
                        "label": agent_name,
                        "x": 350 + (idx * 150),
                        "y": 50 + (idx % 2) * 40,
                        "type": "agent",
                    }
                )

                # Add edge
                prev_node_id = "ai" if idx == 0 else f"agent_{agents_used[idx - 1]}"

                diagram_edges.append({"from": prev_node_id, "to": node_id})

            logger.info(f"✓ Agent delegation complete: {delegation_result['status']}")

            return {
                "messages": [AIMessage(content=final_answer)],
                "agent_delegation": delegation_result,
                "use_agents": True,
                "animation_steps": animation_steps,
                "diagram_nodes": diagram_nodes,
                "diagram_edges": diagram_edges,
            }

        except Exception as e:
            logger.error(f"Error during agent delegation: {str(e)}", exc_info=True)
            # Fall back to tool execution on error
            return {
                "messages": [
                    AIMessage(
                        content=f"Agent delegation failed: {str(e)}. Falling back to tool execution."
                    )
                ],
                "use_agents": False,
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

    def _strategy_selection_node(self, state: AgentState) -> dict[str, Any]:
        """
        Tree of Thoughts - Evaluate multiple strategies and select the best one.

        This node generates 3-5 candidate strategies, evaluates each against
        task requirements, and selects the optimal approach based on user
        preferences and task characteristics.

        Args:
            state: Current agent state

        Returns:
            Updated state with selected strategy
        """
        logger.info("🔵 Strategy selection node called")

        if not self.tot:
            logger.info(
                "⏭️ ToT not initialized yet, skipping strategy selection (will use default strategy)"
            )
            # Return state unchanged to continue workflow
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        # Extract user task
        user_task = None
        for msg in state.get("messages", []):
            if isinstance(msg, HumanMessage):
                user_task = msg.content
                break

        if not user_task:
            logger.debug("No user task found for strategy selection")
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        # Get user preferences from state (if any)
        user_preferences = state.get("user_preferences", {})

        try:
            logger.info(f"🌳 Starting strategy evaluation for task: {user_task[:100]}...")

            # Evaluate strategies
            evaluation = self.tot.evaluate_strategies(
                task=user_task,
                num_strategies=3,
                user_preferences=user_preferences,
                context={"conversation_history": state.get("messages", [])},
            )

            selected = evaluation.selected_strategy

            logger.info(
                f"🌳 Strategy selected: {selected.name} "
                f"(score: {selected.overall_score:.2f}, type: {selected.strategy_type.value})"
            )

            # Create animation step
            animation_steps = state.get("animation_steps", []).copy()
            animation_steps.append(
                {
                    "step": len(animation_steps) + 1,
                    "title": "Strategy Selection",
                    "description": f"Selected: {selected.name} - {selected.description}",
                    "duration": 1500,
                    "icon": "🌳",
                    "bgColor": "#e8f5e8",
                }
            )

            # Convert dataclass to dict for state storage
            from dataclasses import asdict

            return {
                "selected_strategy": asdict(selected),
                "strategy_evaluation": asdict(evaluation),
                "animation_steps": animation_steps,
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        except Exception as e:
            logger.error(f"❌ Strategy selection failed: {e}", exc_info=True)
            # Return state unchanged to continue workflow
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

    def _planning_node(self, state: AgentState) -> dict[str, Any]:
        """
        ReWOO - Generate execution plan upfront.

        This node creates a complete execution plan before tool execution,
        reducing the need for iterative LLM calls during execution.

        Args:
            state: Current agent state

        Returns:
            Updated state with execution plan
        """
        logger.info("🔵 Planning node called")

        if not self.rewoo:
            logger.info(
                "⏭️ ReWOO not initialized yet, skipping planning (will use reactive execution)"
            )
            # Return state unchanged to continue workflow
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        # Extract user task
        user_task = None
        for msg in state.get("messages", []):
            if isinstance(msg, HumanMessage):
                user_task = msg.content
                break

        if not user_task:
            logger.debug("No user task found for planning")
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        # Build context from selected strategy (if available)
        context = {}
        selected_strategy = state.get("selected_strategy")
        if selected_strategy:
            context["strategy"] = selected_strategy.get("strategy_type")
            context["estimated_duration"] = selected_strategy.get("estimated_duration")
            logger.debug(f"Using strategy context: {context}")

        try:
            logger.info(f"📋 Starting plan generation for task: {user_task[:100]}...")

            # Generate plan
            plan = self.rewoo.generate_plan(task=user_task, context=context, max_steps=10)

            logger.info(
                f"📋 Plan generated: {len(plan.steps)} steps "
                f"(confidence: {plan.confidence:.2f}, cached: {plan.cached})"
            )

            # Create animation step
            animation_steps = state.get("animation_steps", []).copy()
            animation_steps.append(
                {
                    "step": len(animation_steps) + 1,
                    "title": "Execution Planning",
                    "description": f"Generated {len(plan.steps)}-step plan with {plan.confidence:.0%} confidence",
                    "duration": 1500,
                    "icon": "📋",
                    "bgColor": "#e3f2fd",
                }
            )

            # Convert plan to dict for state storage
            from dataclasses import asdict

            return {
                "execution_plan": asdict(plan),
                "plan_steps": [asdict(step) for step in plan.steps],
                "animation_steps": animation_steps,
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

        except Exception as e:
            logger.error(f"❌ Planning failed: {e}", exc_info=True)
            # Return state unchanged to continue workflow
            return {
                "animation_steps": state.get("animation_steps", []),
                "diagram_nodes": state.get("diagram_nodes", []),
                "diagram_edges": state.get("diagram_edges", []),
            }

    def _reflection_node(self, state: AgentState) -> dict[str, Any]:
        """
        Self-Reflection node - critiques and improves execution.

        This node analyzes the results of tool execution using the Self-Reflection
        module. If gaps are detected (e.g., missed ports, incomplete data),
        it generates new tool calls to fix them automatically.

        Args:
            state: Current agent state

        Returns:
            Updated state with critique and potential new tool calls
        """
        # Initialize reflection service if needed
        if not self.reflection and self.llm_provider:
            # We need a LangChain-compatible LLM for the service
            # For now, we'll assume the provider has a .llm property or similar
            # If not, we might need an adapter.
            # The current LLMProvider wraps the call, so we pass the provider itself
            # and let the service handle it, or we pass a wrapper.
            # NOTE: The reasoning modules expect a LangChain BaseChatModel.
            # We will use the provider's underlying model if available, or a wrapper.
            # For this implementation, we'll assume the provider IS compatible or we wrap it.
            # Since LLMProvider is custom, we'll use a simple adapter.
            # Temporary: Use the provider directly if it supports invoke
            self.reflection = get_self_reflection(self.llm_provider)

        if not self.reflection:
            logger.warning("Reflection service not available (no LLM)")
            return {"reflection_count": state.get("reflection_count", 0)}

        # Get context
        messages = state.get("messages", [])
        state.get("tool_calls", [])

        # Extract user task
        user_task = "Unknown task"
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_task = msg.content
                break

        # Extract execution results (last tool output)
        last_message = messages[-1] if messages else None
        execution_results = {}

        if (
            isinstance(last_message, HumanMessage)
            and "TOOL_RESULTS" in str(last_message.content)
            or isinstance(last_message, AIMessage)
        ):
            execution_results = {"output": last_message.content}

        # Perform reflection
        try:
            result = self.reflection.reflect(
                task=user_task,
                execution_results=execution_results,
                trigger=ReflectionTrigger.TASK_COMPLETION,
            )

            logger.info(
                f"🔍 Reflection complete: Score={result.quality_score:.2f}, Gaps={len(result.gaps)}"
            )

            # Update state with results
            reflection_results = state.get("reflection_results", [])
            reflection_results.append(result)

            # If quality is low and we haven't looped too many times, auto-correct
            current_count = state.get("reflection_count", 0)
            MAX_REFLECTIONS = 2

            if result.quality_score < 0.8 and current_count < MAX_REFLECTIONS:
                # Generate improvements
                improvements = result.get_high_priority_actions()
                if improvements:
                    logger.info(f"🛠️ Auto-correcting with {len(improvements)} actions")

                    # Convert improvements to tool calls
                    new_tool_calls = []
                    critique_text = "🔍 **Self-Correction Triggered**\n\nI detected some gaps in the previous execution:\n"

                    for gap in result.gaps:
                        critique_text += f"- {gap.description}\n"

                    critique_text += "\nI am automatically running the following fixes:\n"

                    for imp in improvements:
                        critique_text += f"- {imp.description} (using `{imp.tool_name}`)\n"
                        new_tool_calls.append((imp.tool_name, imp.parameters))

                    # Create a message to inform the user (and LLM)
                    AIMessage(content=critique_text)

                    # We need to construct a message that LOOKS like it has tool calls
                    # so the 'tools' node picks it up.
                    # The 'tools' node parses tool calls from the last message.
                    # We'll format the critique message to include the tool calls in the expected format.
                    # Or better, we manually inject the tool calls into the state for the next step.
                    # But 'tools' node reads from message content.

                    # Let's format the tool calls into the message content
                    tool_call_text = ""
                    for name, args in new_tool_calls:
                        tool_call_text += (
                            f"TOOL: {name}({', '.join(f'{k}={v}' for k, v in args.items())})\n"
                        )

                    final_msg = AIMessage(content=f"{critique_text}\n\n{tool_call_text}")

                    return {
                        "messages": [final_msg],
                        "reflection_count": current_count + 1,
                        "reflection_results": reflection_results,
                    }

            # If good enough or max retries reached
            return {"reflection_count": current_count, "reflection_results": reflection_results}

        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            return {"reflection_count": state.get("reflection_count", 0)}

    def _create_workflow(self):
        """
        Create and configure the orchestrator workflow with multi-agent supervision.

        Workflow:
            1. User message -> agent (LLM decides)
            2. Agent -> Check if should delegate to specialized agents
            3a. If yes -> delegate (supervisor routes to specialized agents)
            3b. If no -> tools (execute tools directly)
            4. Results -> back to agent for final synthesis

        Returns:
            Compiled workflow with checkpointing, approval gates, and agent delegation
        """
        # Build graph with Advanced Reasoning Patterns
        workflow = StateGraph(AgentState)

        # Add all nodes
        workflow.add_node("strategy_selection", self._strategy_selection_node)
        workflow.add_node("planning", self._planning_node)
        workflow.add_node("agent", self._call_model)
        workflow.add_node("delegate", self._delegate_to_agents)
        workflow.add_node("tools", self._call_tools)
        workflow.add_node("approval_gate", self._approval_gate)
        workflow.add_node("reflection", self._reflection_node)

        # Set entry point to strategy selection (Phase 3.2)
        workflow.set_entry_point("strategy_selection")

        # Strategy Selection → Planning
        workflow.add_edge("strategy_selection", "planning")

        # Planning → Agent
        workflow.add_edge("planning", "agent")

        # Add conditional edges with approval gate and delegation support
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "delegate": "delegate",
                "tools": "tools",
                "approval_gate": "approval_gate",
                "end": END,
            },
        )

        # Add conditional edges from approval gate
        workflow.add_conditional_edges(
            "approval_gate", self._check_approval, {"approved": "tools", "rejected": END}
        )

        # After tools execute, route to reflection
        workflow.add_edge("tools", "reflection")

        # After reflection, check if we need to loop back to tools or go to agent
        def _after_reflection_routing(state: AgentState) -> Literal["tools", "agent", "end"]:
            """Route after reflection."""
            messages = state.get("messages", [])
            last_msg = messages[-1]

            # If the last message contains TOOL calls (injected by reflection), go to tools
            if isinstance(last_msg, AIMessage) and "TOOL:" in last_msg.content:
                return "tools"

            # Otherwise, go back to agent for final synthesis
            return "agent"

        workflow.add_conditional_edges(
            "reflection",
            _after_reflection_routing,
            {"tools": "tools", "agent": "agent", "end": END},
        )

        # After agent delegation, go to END (agents provide final answer)
        workflow.add_edge("delegate", END)

        # Get checkpointer for state persistence
        # Checkpointing is REQUIRED for approval gates to work
        try:
            self.checkpointer = get_checkpointer()
            if self.checkpointer is not None:
                logger.info(
                    "✅ Workflow compiled with Advanced Reasoning (ToT+ReWOO+Reflection), multi-agent supervision, PostgreSQL checkpointing, and approval gates"
                )
                return workflow.compile(
                    checkpointer=self.checkpointer, interrupt_after=["approval_gate"]
                )
            else:
                logger.warning(
                    "⚠️ No checkpointer available - approval gates will not work properly!"
                )
                logger.warning("   Approval gates require checkpointing for state persistence")
                return workflow.compile()
        except Exception as e:
            logger.error(f"Checkpointer initialization error: {e}")
            logger.error("⚠️ Approval gates will not work without checkpointing!")
            return workflow.compile()

    async def run(
        self,
        message: str,
        user_id: int,
        db: AsyncSession,
        history: Optional[list] = None,
        conversation_id: Optional[int] = None,
        thread_id: Optional[str] = None,
    ) -> Union[str, dict[str, Any]]:
        """
        Run the orchestrator with a message and optional history.

        Args:
            message: User message
            user_id: User ID for loading LLM configuration
            db: Database session
            history: Optional conversation history
            conversation_id: Optional conversation ID for thread tracking
            thread_id: Optional custom thread ID (defaults to user_id_conv_id format)

        Returns:
            Response string or dict with animation data
        """

        # Load user's active LLM provider from database
        from app.services.llm.db_factory import get_db_provider_factory

        factory = get_db_provider_factory()
        llm_provider = await factory.get_active_provider(db, user_id)

        if not llm_provider:
            raise ValueError(
                "No active LLM model configured. Please configure an API key and activate a model in settings."
            )

        # Set the provider for this request
        self.llm_provider = llm_provider

        # Initialize reasoning services with the provider
        # We wrap the provider to match the LangChain interface expected by reasoning modules
        from app.services.llm.providers.base import LangChainAdapter

        langchain_llm = LangChainAdapter(llm_provider)

        self.reflection = get_self_reflection(langchain_llm)
        self.rewoo = get_rewoo_planner(langchain_llm, self.tool_registry.get_all_tools())
        self.tot = get_tree_of_thoughts(langchain_llm)

        # Store user_id and conversation_id for auto-injection into memory tools
        self.current_user_id = user_id
        self.current_conversation_id = conversation_id

        # Create thread_id for checkpointing if not provided
        if thread_id is None:
            if conversation_id is not None:
                thread_id = f"user_{user_id}_conv_{conversation_id}"
            else:
                thread_id = f"user_{user_id}"

        logger.info(f"Running orchestrator for user {user_id} with thread_id: {thread_id}")
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
            # Prepare config for checkpointing
            config = {"configurable": {"thread_id": thread_id}} if self.checkpointer else None

            # Run agent with animation/diagram tracking and checkpointing
            invoke_kwargs = {
                "messages": messages,
                "tool_calls": [],
                "animation_steps": [],
                "diagram_nodes": [],
                "diagram_edges": [],
                # Advanced Reasoning Patterns (Phase 3.2)
                "selected_strategy": {},
                "strategy_evaluation": {},
                "execution_plan": {},
                "plan_steps": [],
                "user_preferences": {},  # Can be populated from user settings
                "reasoning_metrics": {},
            }

            # Invoke with config if checkpointing is enabled
            if config:
                result = self.workflow.invoke(invoke_kwargs, config=config)
                logger.debug(f"Workflow executed with checkpointing (thread: {thread_id})")
            else:
                result = self.workflow.invoke(invoke_kwargs)
                logger.debug("Workflow executed without checkpointing")

            # Extract final response
            final_message = result["messages"][-1]
            content = (
                final_message.content if hasattr(final_message, "content") else str(final_message)
            )

            # Clean up the response
            cleaned_content = clean_response(content)

            logger.info(
                f"Orchestrator response: {cleaned_content[:200]}..."
                if len(cleaned_content) > 200
                else cleaned_content
            )

            # Check if we have animation steps (tool execution occurred)
            animation_steps = result.get("animation_steps", [])
            diagram_nodes = result.get("diagram_nodes", [])
            diagram_edges = result.get("diagram_edges", [])

            if animation_steps:
                # Add initial nodes for user and AI
                initial_nodes = [
                    {"id": "user", "label": "User Query", "x": 50, "y": 50, "type": "user"},
                    {"id": "ai", "label": "AI Agent", "x": 200, "y": 50, "type": "ai"},
                ]

                # Add result node
                result_node = {
                    "id": "result",
                    "label": "Final Answer",
                    "x": 350 + (len(diagram_nodes) * 150),
                    "y": 50,
                    "type": "result",
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

                logger.info(
                    f"Generated {len(animation_steps)} animation steps and diagram with {len(all_nodes)} nodes"
                )

                return {
                    "animation_steps": animation_steps,
                    "diagram": {"nodes": all_nodes, "edges": all_edges},
                    "final_answer": cleaned_content,
                }

            # Check if workflow is paused at approval gate
            if result.get("approval_status") == "pending" and result.get("pending_approval"):
                logger.info("Workflow paused at approval gate, returning approval request")
                # Extract the approval message content
                approval_message = result["messages"][-1]
                content = (
                    approval_message.content
                    if hasattr(approval_message, "content")
                    else str(approval_message)
                )

                return {
                    "pending_approval": result["pending_approval"],
                    "approval_status": "pending",
                    "messages": [{"content": content}],  # Format for frontend
                    "final_answer": content,
                }

            # No tools were executed, return regular response
            return cleaned_content

        except Exception as e:
            logger.error(f"Error in orchestrator: {str(e)}", exc_info=True)
            raise


# Global orchestrator instance
_orchestrator_service: Optional[OrchestratorService] = None


def reset_orchestrator_service():
    """Reset the global orchestrator service instance (for testing/reload)."""
    global _orchestrator_service
    _orchestrator_service = None
    logger.info("🔄 Orchestrator service reset - will recreate on next request")


def get_orchestrator_service() -> OrchestratorService:
    """
    Get or create global orchestrator service instance.

    Returns:
        OrchestratorService instance
    """
    global _orchestrator_service
    # TEMPORARY: Always recreate to pick up new workflow
    # TODO: Remove this after Phase 3.2 is stable
    if _orchestrator_service is None:
        logger.info("🆕 Creating new orchestrator service instance")
        _orchestrator_service = OrchestratorService()
    return _orchestrator_service


async def run_orchestrator(
    message: str,
    user_id: int,
    db: AsyncSession,
    history: Optional[list] = None,
    conversation_id: Optional[int] = None,
) -> Union[str, dict[str, Any]]:
    """
    Run the orchestrator with a message and optional history.

    This is a convenience function that uses the global orchestrator instance.

    Args:
        message: User message
        user_id: User ID for loading LLM configuration
        db: Database session
        history: Optional conversation history
        conversation_id: Optional conversation ID for checkpoint tracking

    Returns:
        Response string or dict with animation data
    """
    orchestrator = get_orchestrator_service()
    return await orchestrator.run(message, user_id, db, history, conversation_id)
