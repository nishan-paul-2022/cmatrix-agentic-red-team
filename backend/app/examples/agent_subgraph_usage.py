"""
Example: Using Agent Subgraphs

This example demonstrates how to use the new agent subgraphs
for autonomous security assessments.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.registry import get_agent_registry, AgentRegistry
from app.agents.specialized.network_agent import create_network_agent
from app.agents.specialized.web_agent import create_web_agent
from app.agents.specialized.vuln_intel_agent import create_vuln_intel_agent
from app.services.llm.pool import get_llm_pool


async def example_1_direct_agent_usage(db: AsyncSession, user_id: int):
    """
    Example 1: Using agents directly without the registry.
    
    This is useful when you know exactly which agent you need.
    """
    print("=" * 60)
    print("Example 1: Direct Agent Usage")
    print("=" * 60)
    
    # Get LLM pool
    llm_pool = get_llm_pool()
    
    # Get LLM provider for network agent
    llm_provider = await llm_pool.get_provider("network_agent", db, user_id)
    
    # Create network agent
    network_agent = create_network_agent(llm_provider)
    
    # Invoke the agent with a task
    result = await network_agent.ainvoke(
        task="Scan localhost for open ports in the range 1-1024",
        context={"priority": "high"}
    )
    
    # Print results
    print("\n📊 Agent Results:")
    print(f"  Completed: {result['completed']}")
    print(f"  Reasoning Iterations: {result['metadata']['reasoning_iterations']}")
    print(f"  Tools Executed: {result['metadata']['tools_executed']}")
    
    if result.get('error'):
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success!")
        
        # Print final message
        if result['messages']:
            final_message = result['messages'][-1]
            print(f"\n💬 Final Response:")
            print(f"  {final_message.content[:200]}...")
    
    return result


async def example_2_registry_based_usage(db: AsyncSession, user_id: int):
    """
    Example 2: Using the agent registry for automatic agent selection.
    
    This is the recommended approach for production use.
    """
    print("\n" + "=" * 60)
    print("Example 2: Registry-Based Usage")
    print("=" * 60)
    
    # Get agent registry
    registry = get_agent_registry()
    
    # User query
    user_query = "Check for recent CVEs related to Apache web server"
    
    # Automatically select the best agent
    selected_agent = registry.select_agent(user_query)
    print(f"\n🤖 Selected Agent: {selected_agent}")
    
    # Get agent info
    agent_info = registry.get_agent_info(selected_agent)
    print(f"  Name: {agent_info['name']}")
    print(f"  Description: {agent_info['description']}")
    
    # Invoke the agent
    result = await registry.invoke_agent(
        agent_type=selected_agent,
        task=user_query,
        context={"user_query": user_query},
        db=db,
        user_id=user_id
    )
    
    # Print results
    print("\n📊 Agent Results:")
    print(f"  Completed: {result['completed']}")
    print(f"  Agent: {result['metadata']['agent_name']}")
    
    return result


async def example_3_multiple_agents_parallel(db: AsyncSession, user_id: int):
    """
    Example 3: Running multiple agents in parallel.
    
    This demonstrates the power of the multi-agent system.
    """
    print("\n" + "=" * 60)
    print("Example 3: Parallel Multi-Agent Execution")
    print("=" * 60)
    
    # Get agent registry
    registry = get_agent_registry()
    
    # Define tasks for different agents
    tasks = [
        {
            "agent": AgentRegistry.NETWORK_AGENT,
            "task": "Scan example.com for open ports",
            "context": {}
        },
        {
            "agent": AgentRegistry.WEB_AGENT,
            "task": "Check SSL/TLS security of https://example.com",
            "context": {}
        },
        {
            "agent": AgentRegistry.VULN_INTEL_AGENT,
            "task": "Search for recent critical CVEs in the last 7 days",
            "context": {}
        }
    ]
    
    # Run all agents in parallel
    print("\n🚀 Launching 3 agents in parallel...")
    
    results = await asyncio.gather(*[
        registry.invoke_agent(
            agent_type=task["agent"],
            task=task["task"],
            context=task["context"],
            db=db,
            user_id=user_id
        )
        for task in tasks
    ])
    
    # Print results
    print("\n📊 Results from all agents:")
    for i, (task, result) in enumerate(zip(tasks, results), 1):
        print(f"\n  Agent {i}: {task['agent']}")
        print(f"    Task: {task['task']}")
        print(f"    Completed: {result['completed']}")
        print(f"    Iterations: {result['metadata']['reasoning_iterations']}")
        print(f"    Tools Used: {result['metadata']['tools_executed']}")
    
    return results


async def example_4_agent_capabilities(db: AsyncSession, user_id: int):
    """
    Example 4: Exploring agent capabilities.
    
    This shows how to discover what agents are available and what they can do.
    """
    print("\n" + "=" * 60)
    print("Example 4: Agent Capabilities Discovery")
    print("=" * 60)
    
    # Get agent registry
    registry = get_agent_registry()
    
    # Get all available agents
    available_agents = registry.get_available_agents()
    print(f"\n📋 Available Agents: {len(available_agents)}")
    
    # Print info for each agent
    for agent_type in available_agents:
        info = registry.get_agent_info(agent_type)
        print(f"\n🤖 {info['name']}")
        print(f"  Type: {agent_type}")
        print(f"  Description: {info['description']}")
        print(f"  Capabilities:")
        for capability in info['capabilities']:
            print(f"    • {capability}")
        print(f"  Keywords: {', '.join(info['keywords'][:5])}...")


async def example_5_error_handling(db: AsyncSession, user_id: int):
    """
    Example 5: Error handling and recovery.
    
    This demonstrates how agents handle errors gracefully.
    """
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    # Get LLM pool
    llm_pool = get_llm_pool()
    
    try:
        # Try to get provider for invalid agent
        llm_provider = await llm_pool.get_provider("invalid_agent", db, user_id)
    except ValueError as e:
        print(f"\n❌ Expected error caught: {e}")
    
    # Get valid provider
    llm_provider = await llm_pool.get_provider("network_agent", db, user_id)
    network_agent = create_network_agent(llm_provider)
    
    # Invoke with a task that might fail
    result = await network_agent.ainvoke(
        task="Scan an invalid target that doesn't exist",
        context={}
    )
    
    # Check for errors in result
    if result.get('error'):
        print(f"\n⚠️  Agent encountered an error: {result['error']}")
        print("  But the workflow completed gracefully!")
    else:
        print("\n✅ Agent completed successfully")
    
    return result


# Main execution
async def main():
    """
    Main function to run all examples.
    
    Note: In production, you would get db and user_id from your application context.
    """
    print("\n" + "=" * 60)
    print("🚀 Agent Subgraph Examples")
    print("=" * 60)
    
    # Mock database session and user_id for examples
    # In production, use: db = get_async_session(), user_id = current_user.id
    db = None  # Replace with actual AsyncSession
    user_id = 1  # Replace with actual user ID
    
    print("\n⚠️  Note: These examples require a database connection and user ID.")
    print("   Update the db and user_id variables in main() to run.")
    
    # Uncomment to run examples (after setting up db and user_id):
    # await example_1_direct_agent_usage(db, user_id)
    # await example_2_registry_based_usage(db, user_id)
    # await example_3_multiple_agents_parallel(db, user_id)
    # await example_4_agent_capabilities(db, user_id)
    # await example_5_error_handling(db, user_id)


if __name__ == "__main__":
    asyncio.run(main())
