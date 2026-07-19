from core.genesis.workforce_activation_bridge import (
    workforce_activation_bridge
)


print("=" * 50)
print("⚡ GENESIS WORKFORCE ACTIVATION BRIDGE TEST")
print("=" * 50)


agents = [

    {
        "name": "Sales Agent",
        "role": "Sales Intelligence",
        "skills": [
            "sales",
            "crm",
            "lead_generation"
        ]
    },

    {
        "name": "Coding Agent",
        "role": "Software Engineer",
        "skills": [
            "coding",
            "automation",
            "deployment"
        ]
    }

]


result = workforce_activation_bridge.activate_workforce(
    agents
)


print(result)


print(
    workforce_activation_bridge.report()
)
