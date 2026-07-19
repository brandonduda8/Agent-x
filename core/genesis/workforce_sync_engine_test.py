from core.genesis.workforce_sync_engine import (
    workforce_sync_engine
)


print("=" * 50)
print("🔄 GENESIS WORKFORCE SYNC ENGINE TEST")
print("=" * 50)


agents = [

    {
        "name": "Coding Agent",
        "skills": [
            "coding",
            "automation",
            "deployment"
        ]
    },

    {
        "name": "Revenue Agent",
        "skills": [
            "sales",
            "crm",
            "lead_generation"
        ]
    }

]


result = workforce_sync_engine.sync_workforce(
    agents
)


print()

print(result)

print()

print(
    workforce_sync_engine.status()
)
