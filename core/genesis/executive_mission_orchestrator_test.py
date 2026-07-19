from core.genesis.executive_mission_orchestrator import (
    executive_mission_orchestrator
)


print("=" * 50)
print("🎯 GENESIS EXECUTIVE MISSION ORCHESTRATOR TEST")
print("=" * 50)


mission = executive_mission_orchestrator.create_mission(
    "Acquire first AI automation customers"
)


print()

print(mission)

print()

print(
    executive_mission_orchestrator.status()
)
