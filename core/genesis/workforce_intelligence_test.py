from core.genesis.workforce_intelligence import (
    workforce_intelligence
)


print("=" * 60)
print("🧬 GENESIS WORKFORCE INTELLIGENCE TEST")
print("=" * 60)


workforce_intelligence.remember_agent(
    {
        "id":"agent_demo",
        "name":"Sales Agent",
        "skills":[
            "sales",
            "crm",
            "lead_generation"
        ]
    }
)


result = workforce_intelligence.activate_existing(
    "sales"
)


print(result)

print(
    workforce_intelligence.report()
)
