"""Base agent subgraph implementation."""

from abc import ABC, abstractmethod
from typing import Any, Literal

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from loguru import logger

from app.agents.base.state import SubgraphState
from app.services.llm.providers.base import LLMProvider, Message


class BaseAgentSubgraph(ABC):
    """
    Base class for all specialized agent subgraphs.

    This class provides the foundation for creating autonomous agent subgraphs
    with their own reasoning loops, tool execution, and result synthesis.

    Each specialized agent (Network, Web, VulnIntel) extends this class and
    implements the abstract methods to define agent-specific behavior.
    """

    def __init__(self, llm_provider: LLMProvider, agent_name: str):
        """
        Initialize the agent subgraph.

        Args:
            llm_provider: LLM provider instance for this agent
            agent_name: Name of the agent (for logging and identification)
        """
        self.llm_provider = llm_provider
        self.agent_name = agent_name
        self.tools = self._register_tools()
        self.workflow = self._create_workflow()
        logger.info(f"Initialized {agent_name} subgraph with {len(self.tools)} tools")

    @abstractmethod
    def _register_tools(self) -> list[dict[str, Any]]:
        """
        Register agent-specific tools.

        Returns:
            List of tool dictionaries with 'name', 'function', and 'description'
        """
        pass

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.

        Returns:
            System prompt string defining agent's role and capabilities
        """
        pass

    def _reason(self, state: SubgraphState) -> dict[str, Any]:
        """
        Agent reasoning step - decides what to do next.

        This is the core decision-making node where the agent's LLM
        analyzes the task and decides whether to use tools or synthesize results.

        Args:
            state: Current subgraph state

        Returns:
            Updated state with agent's reasoning
        """
        try:
            messages = list(state.get("messages", []))
            task = state.get("task", "")
            context = state.get("context", {})
            results = state.get("results", [])

            # Build the prompt
            if not messages:
                # First reasoning iteration
                system_prompt = self._get_system_prompt()

                # Add tool definitions
                tool_definitions = self._format_tool_definitions()
                system_prompt += f"\n\n{tool_definitions}"

                messages.append(SystemMessage(content=system_prompt))

                # Add task as user message
                task_message = f"Task: {task}"
                if context:
                    task_message += f"\n\nContext: {context}"
                messages.append(HumanMessage(content=task_message))
            else:
                # Subsequent iterations - add tool results if any
                if results:
                    latest_results = results[-1]
                    result_message = f"Tool execution results:\n{latest_results}"
                    messages.append(HumanMessage(content=result_message))

            # Convert to provider messages
            provider_messages = self._convert_messages(messages)

            # Call LLM
            response = self.llm_provider.invoke(provider_messages)

            if not response or not response.strip():
                logger.warning(f"{self.agent_name}: LLM returned empty response")
                response = "I need more information to complete this task."

            # Add AI response to messages
            messages.append(AIMessage(content=response))

            # Parse tool calls from response
            from app.tools.execution import parse_tool_calls

            tool_calls = parse_tool_calls(response)

            logger.info(
                f"{self.agent_name}: Reasoning complete, found {len(tool_calls)} tool calls"
            )

            return {
                "messages": messages,
                "tool_calls": tool_calls,
                "metadata": {
                    **state.get("metadata", {}),
                    "reasoning_iterations": state.get("metadata", {}).get("reasoning_iterations", 0)
                    + 1,
                },
            }

        except Exception as e:
            logger.error(f"{self.agent_name}: Error in reasoning: {e}", exc_info=True)
            return {"error": f"Reasoning error: {str(e)}", "completed": True}

    def _execute_tools(self, state: SubgraphState) -> dict[str, Any]:
        """
        Execute tools based on agent's reasoning.

        Args:
            state: Current subgraph state

        Returns:
            Updated state with tool execution results
        """
        try:
            tool_calls = state.get("tool_calls", [])
            results = list(state.get("results", []))

            if not tool_calls:
                logger.warning(f"{self.agent_name}: No tool calls to execute")
                return {"results": results}

            execution_results = []

            for tool_name, tool_args in tool_calls:
                logger.info(f"{self.agent_name}: Executing {tool_name} with args {tool_args}")

                # Find the tool
                tool = self._find_tool(tool_name)

                if not tool:
                    error_msg = f"Tool '{tool_name}' not found in {self.agent_name}"
                    logger.error(error_msg)
                    execution_results.append(
                        {"tool": tool_name, "status": "error", "error": error_msg}
                    )
                    continue

                try:
                    # Execute the tool
                    func = tool["function"]

                    if hasattr(func, "invoke"):
                        result = func.invoke(tool_args)
                    else:
                        result = func(**tool_args)

                    execution_results.append(
                        {
                            "tool": tool_name,
                            "status": "success",
                            "result": result,
                            "args": tool_args,
                        }
                    )

                    logger.info(f"{self.agent_name}: Successfully executed {tool_name}")

                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    logger.error(f"{self.agent_name}: {error_msg}", exc_info=True)
                    execution_results.append(
                        {
                            "tool": tool_name,
                            "status": "error",
                            "error": error_msg,
                            "args": tool_args,
                        }
                    )

            results.append({"execution_batch": len(results) + 1, "results": execution_results})

            return {
                "results": results,
                "tool_calls": [],  # Clear tool calls after execution
                "metadata": {
                    **state.get("metadata", {}),
                    "tools_executed": state.get("metadata", {}).get("tools_executed", 0)
                    + len(tool_calls),
                },
            }

        except Exception as e:
            logger.error(f"{self.agent_name}: Error executing tools: {e}", exc_info=True)
            return {"error": f"Tool execution error: {str(e)}", "completed": True}

    def _synthesize(self, state: SubgraphState) -> dict[str, Any]:
        """
        Synthesize results and prepare final response.

        This node creates the final output from the agent, summarizing
        all tool executions and providing actionable insights.

        Args:
            state: Current subgraph state

        Returns:
            Updated state with final synthesis
        """
        try:
            messages = list(state.get("messages", []))
            results = state.get("results", [])

            # If we have an error, return it
            if state.get("error"):
                return {"completed": True}

            # If no results, the agent completed without tools
            if not results:
                logger.info(f"{self.agent_name}: No tool results to synthesize")
                return {"completed": True}

            # Ask LLM to synthesize the results
            synthesis_prompt = (
                "Based on the tool execution results above, provide a comprehensive "
                "summary and analysis. Include:\n"
                "1. Key findings\n"
                "2. Security implications (if any)\n"
                "3. Recommended actions\n"
                "4. Any additional insights"
            )

            messages.append(HumanMessage(content=synthesis_prompt))

            # Convert and call LLM
            provider_messages = self._convert_messages(messages)
            synthesis = self.llm_provider.invoke(provider_messages)

            messages.append(AIMessage(content=synthesis))

            logger.info(f"{self.agent_name}: Synthesis complete")

            return {
                "messages": messages,
                "completed": True,
                "metadata": {**state.get("metadata", {}), "synthesis_complete": True},
            }

        except Exception as e:
            logger.error(f"{self.agent_name}: Error in synthesis: {e}", exc_info=True)
            return {"error": f"Synthesis error: {str(e)}", "completed": True}

    def _should_use_tools(self, state: SubgraphState) -> Literal["tools", "synthesize"]:
        """
        Decide whether to execute tools or move to synthesis.

        Args:
            state: Current subgraph state

        Returns:
            Next step: "tools" or "synthesize"
        """
        tool_calls = state.get("tool_calls", [])

        if tool_calls:
            logger.debug(f"{self.agent_name}: Routing to tool execution")
            return "tools"

        logger.debug(f"{self.agent_name}: Routing to synthesis")
        return "synthesize"

    def _should_continue_reasoning(self, state: SubgraphState) -> Literal["reason", "synthesize"]:
        """
        Decide whether to continue reasoning or move to synthesis.

        Args:
            state: Current subgraph state

        Returns:
            Next step: "reason" or "synthesize"
        """
        # Check iteration limit
        max_iterations = 5
        current_iterations = state.get("metadata", {}).get("reasoning_iterations", 0)

        if current_iterations >= max_iterations:
            logger.warning(f"{self.agent_name}: Max reasoning iterations reached")
            return "synthesize"

        # Check if we have results to analyze
        results = state.get("results", [])
        if results:
            # We executed tools, continue reasoning to analyze results
            logger.debug(f"{self.agent_name}: Continuing reasoning to analyze results")
            return "reason"

        # No more work to do
        return "synthesize"

    def _create_workflow(self) -> StateGraph:
        """
        Create the agent's workflow graph.

        Returns:
            Compiled StateGraph workflow
        """
        workflow = StateGraph(SubgraphState)

        # Add nodes
        workflow.add_node("reason", self._reason)
        workflow.add_node("execute_tools", self._execute_tools)
        workflow.add_node("synthesize", self._synthesize)

        # Set entry point
        workflow.set_entry_point("reason")

        # Add conditional edges
        workflow.add_conditional_edges(
            "reason", self._should_use_tools, {"tools": "execute_tools", "synthesize": "synthesize"}
        )

        workflow.add_conditional_edges(
            "execute_tools",
            self._should_continue_reasoning,
            {"reason": "reason", "synthesize": "synthesize"},
        )

        workflow.add_edge("synthesize", END)

        logger.debug(f"{self.agent_name}: Workflow graph created")
        return workflow.compile()

    def invoke(self, task: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Invoke the agent subgraph synchronously.

        Args:
            task: The task to execute
            context: Additional context for the task

        Returns:
            Final state with results
        """
        initial_state: SubgraphState = {
            "messages": [],
            "task": task,
            "context": context or {},
            "results": [],
            "metadata": {
                "agent_name": self.agent_name,
                "reasoning_iterations": 0,
                "tools_executed": 0,
            },
            "error": "",
            "completed": False,
            "tool_calls": [],
        }

        logger.info(f"{self.agent_name}: Starting task execution: {task[:100]}...")

        try:
            final_state = self.workflow.invoke(initial_state)
            logger.info(f"{self.agent_name}: Task completed successfully")
            return final_state
        except Exception as e:
            logger.error(f"{self.agent_name}: Task execution failed: {e}", exc_info=True)
            return {**initial_state, "error": str(e), "completed": True}

    async def ainvoke(self, task: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Invoke the agent subgraph asynchronously.

        Args:
            task: The task to execute
            context: Additional context for the task

        Returns:
            Final state with results
        """
        initial_state: SubgraphState = {
            "messages": [],
            "task": task,
            "context": context or {},
            "results": [],
            "metadata": {
                "agent_name": self.agent_name,
                "reasoning_iterations": 0,
                "tools_executed": 0,
            },
            "error": "",
            "completed": False,
            "tool_calls": [],
        }

        logger.info(f"{self.agent_name}: Starting async task execution: {task[:100]}...")

        try:
            final_state = await self.workflow.ainvoke(initial_state)
            logger.info(f"{self.agent_name}: Async task completed successfully")
            return final_state
        except Exception as e:
            logger.error(f"{self.agent_name}: Async task execution failed: {e}", exc_info=True)
            return {**initial_state, "error": str(e), "completed": True}

    # Helper methods

    def _format_tool_definitions(self) -> str:
        """Format tool definitions for the system prompt."""
        if not self.tools:
            return "No tools available."

        definitions = ["Available tools:"]
        for tool in self.tools:
            definitions.append(f"\n- {tool['name']}: {tool.get('description', 'No description')}")

        definitions.append(
            "\n\nTo use a tool, respond with: TOOL: tool_name(param1=value1, param2=value2)"
        )

        return "\n".join(definitions)

    def _find_tool(self, tool_name: str) -> dict[str, Any]:
        """Find a tool by name."""
        for tool in self.tools:
            if tool["name"] == tool_name:
                return tool
        return None

    def _convert_messages(self, messages: list[BaseMessage]) -> list[Message]:
        """Convert LangChain messages to provider messages."""
        provider_messages = []

        for msg in messages:
            if isinstance(msg, SystemMessage):
                provider_messages.append(Message(role="system", content=msg.content))
            elif isinstance(msg, HumanMessage):
                provider_messages.append(Message(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                provider_messages.append(Message(role="assistant", content=msg.content))
            else:
                # Fallback
                provider_messages.append(Message(role="user", content=str(msg.content)))

        return provider_messages
