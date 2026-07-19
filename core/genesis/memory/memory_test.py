from core.genesis.memory.agent_memory import (
    agent_memory
)

from core.genesis.memory.experience_manager import (
    experience_manager
)


print("=" * 50)
print("🧠 GENESIS MEMORY SYSTEM TEST")
print("=" * 50)


experience_manager.record_execution(
    "Revenue Agent",
    "Find AI automation customers",
    {
        "success": True,
        "leads": 25
    }
)


agent_memory.learn(
    "Revenue Agent",
    "AI companies respond better to personalized outreach"
)


print(
    agent_memory.recall(
        "Revenue Agent"
    )
)


print(
    experience_manager.report()
)
