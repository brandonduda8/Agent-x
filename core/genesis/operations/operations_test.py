from core.genesis.operations.operations_controller import (
    operations_controller
)


print("=" * 60)
print("⚙️ GENESIS AUTONOMOUS OPERATIONS CORE TEST")
print("=" * 60)


objective = operations_controller.register_objective(
    "Acquire first AI automation customers"
)


operations_controller.register_agent(
    {
        "name": "Revenue Agent",
        "status": "ACTIVE",
        "skills": [
            "sales",
            "lead_generation",
            "automation"
        ]
    }
)


operations_controller.record_metric(
    "pipeline_value",
    5000
)


cycle = operations_controller.start_cycle(
    objective["objective"]
)


result = operations_controller.complete_cycle(
    cycle,
    {
        "tasks_completed": 6,
        "success": True
    }
)


print(result)

print(
    operations_controller.report()
)
