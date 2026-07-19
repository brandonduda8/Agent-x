from core.genesis.workforce_integration_layer import (
    workforce_integration_layer
)


print("=" * 50)
print("🔗 GENESIS WORKFORCE INTEGRATION LAYER TEST")
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


result = workforce_integration_layer.integrate_workforce(
    agents
)


print()

print(result)

print()

print(
    workforce_integration_layer.report()
)
