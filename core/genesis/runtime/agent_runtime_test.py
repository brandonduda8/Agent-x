from core.genesis.runtime.agent_runtime import (
    agent_runtime
)


print("=" * 60)
print("🤖 GENESIS AGENT RUNTIME TEST")
print("=" * 60)


agent = agent_runtime.create_agent(
    "Sales Agent",
    [
        "sales",
        "analysis",
        "execution"
    ]
)


result = agent_runtime.run(
    agent,
    "Acquire first AI automation customers",
    "lead_generation",
    "Healthcare AI"
)


print(result)


print(agent_runtime.report())
