from core.genesis.workforce_activation_manager import (
    workforce_activation_manager
)


print("=" * 50)
print("⚡ GENESIS WORKFORCE ACTIVATION MANAGER TEST")
print("=" * 50)


agents = [

    {
        "name": "Coding Agent",
        "role": "Software Engineer",
        "skills": [
            "coding",
            "automation",
            "deployment"
        ]
    },

    {
        "name": "Revenue Agent",
        "role": "Sales Intelligence",
        "skills": [
            "sales",
            "crm",
            "lead_generation"
        ]
    }

]


result = workforce_activation_manager.activate_workforce(
    agents
)


print()

print(result)

print()

print(
    workforce_activation_manager.status()
)
