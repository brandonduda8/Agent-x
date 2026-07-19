from core.genesis.executive_controller import executive_controller

from core.genesis.worker_registry import worker_registry
from core.genesis.tool_registry import tool_registry


print("=" * 50)
print("👑 GENESIS EXECUTIVE CONTROLLER TEST")
print("=" * 50)


executive_controller.register(
    "Worker Registry",
    worker_registry
)

executive_controller.register(
    "Tool Registry",
    tool_registry
)


print()

print(executive_controller.boot())

print()

print(
    executive_controller.execute_cycle(
        "Acquire first AI automation customers"
    )
)

print()

print(executive_controller.status())
