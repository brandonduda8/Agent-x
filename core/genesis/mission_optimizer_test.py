from core.genesis.mission_optimizer import (
    mission_optimizer
)


print("=" * 50)
print("🧠 GENESIS MISSION OPTIMIZER TEST")
print("=" * 50)


result = mission_optimizer.optimize(
    "Acquire first AI automation customers"
)


print(result)

print(
    mission_optimizer.report()
)
