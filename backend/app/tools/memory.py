"""Memory tools for the agent."""

from typing import Optional

from langchain.tools import tool

from app.services.vector_store import get_vector_store


@tool
def search_knowledge_base(query: str, user_id: Optional[int] = None) -> str:
    """
    Search the long-term knowledge base for any previously saved information.
    Use this to recall user preferences, past conversations, saved facts, or any stored data.

    Args:
        query: What you want to search for (e.g., "user's name", "user's profession", "previous discussion about X")
        user_id: AUTOMATICALLY INJECTED - Do not provide this parameter

    Returns:
        Relevant information from the knowledge base.

    Example usage:
        search_knowledge_base(query="user's name")
        search_knowledge_base(query="what does the user do for work")
        search_knowledge_base(query="user preferences")
    """
    vector_store = get_vector_store()

    # Build filters
    filters = {}
    if user_id:
        filters["user_id"] = user_id

    results = vector_store.search_memory(
        query,
        limit=5,
        score_threshold=0.2,  # Lower threshold for better recall
        filter_metadata=filters if filters else None,
        use_reranking=True,
    )

    if not results:
        return "No relevant information found in knowledge base."

    summary = "Found the following relevant information:\n"
    for i, res in enumerate(results, 1):
        content = res["content"]
        meta = res["metadata"]
        date = meta.get("created_at", "unknown date")

        summary += f"\n{i}. [{date}] {content}\n"

    return summary


@tool
def save_to_knowledge_base(content: str, user_id: int = None, conversation_id: int = None) -> str:
    """
    Save important information to the long-term knowledge base for future recall.
    Use this to remember user preferences, personal details, important facts, or any information worth remembering.
    Automatically chunks large content for better retrieval.

    Args:
        content: The information to save (REQUIRED - provide this)
        user_id: AUTOMATICALLY INJECTED - Do not provide this parameter
        conversation_id: AUTOMATICALLY INJECTED - Do not provide this parameter

    Returns:
        Confirmation message.

    Example usage:
        save_to_knowledge_base(content="User's name is Neo and they are a software engineer")
        save_to_knowledge_base(content="User prefers dark mode and likes Python programming")
    """
    vector_store = get_vector_store()

    metadata = {"user_id": user_id, "conversation_id": conversation_id, "type": "manual_entry"}

    # Use chunking-aware method
    success = vector_store.add_memory_with_chunking(content, metadata)

    if success:
        return "Successfully saved to knowledge base."
    return "Failed to save to knowledge base."
