"""Base state definition for all agent subgraphs."""

from collections.abc import Sequence
from typing import Any, TypedDict

from langchain_core.messages import BaseMessage


class SubgraphState(TypedDict):
    """
    Base state for all agent subgraphs.

    This state structure is used by all specialized agents to maintain
    consistency across the multi-agent system.

    Attributes:
        messages: Conversation history with the agent
        task: The specific task assigned to this agent
        context: Additional context from the orchestrator
        results: List of results from tool executions
        metadata: Agent-specific metadata (timing, iterations, etc.)
        error: Error message if something went wrong
        completed: Whether the agent has completed its task
        tool_calls: Pending tool calls to execute
    """

    messages: Sequence[BaseMessage]
    task: str
    context: dict[str, Any]
    results: list[dict[str, Any]]
    metadata: dict[str, Any]
    error: str
    completed: bool
    tool_calls: list[tuple]
