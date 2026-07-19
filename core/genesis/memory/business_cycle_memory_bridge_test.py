from core.genesis.memory.business_cycle_memory_bridge import (
    business_cycle_memory_bridge
)


print("=" * 50)
print("🧠 GENESIS BUSINESS CYCLE MEMORY BRIDGE TEST")
print("=" * 50)


result = business_cycle_memory_bridge.record_cycle(
    {
        "objective":
        "Acquire first AI automation customers",

        "status":
        "COMPLETE",

        "execution":
        {
            "successful_tasks": 6
        },

        "learning":
        {
            "performance": 1.0,

            "lesson":
            "Scale outreach workflow"
        }
    }
)


print(result)

print(
    business_cycle_memory_bridge.report()
)
