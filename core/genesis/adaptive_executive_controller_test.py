from core.genesis.adaptive_executive_controller import (
    adaptive_executive_controller
)


print("=" * 60)
print("👑 GENESIS ADAPTIVE EXECUTIVE CONTROLLER TEST")
print("=" * 60)


result = adaptive_executive_controller.run(
    "Acquire first AI automation customers"
)


print(result)

print(
    adaptive_executive_controller.report()
)
