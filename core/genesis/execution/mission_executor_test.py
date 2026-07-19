from core.genesis.execution.mission_executor import (
    mission_executor
)


print("=" * 60)
print("⚡ GENESIS EXECUTION ENGINE TEST")
print("=" * 60)


result = mission_executor.execute(
    "Acquire first AI automation customers",
    "Healthcare AI"
)


print(result)

print(mission_executor.report())
