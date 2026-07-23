from core.genesis.fusion.genesis_fusion_controller import (
    genesis_fusion_controller
)


report = genesis_fusion_controller.scan()

genesis_fusion_controller.save()


print("\n==============================")
print(" GENESIS FUSION AUDIT v1")
print("==============================")

print(
    "Python Files:",
    report["python_files"]
)

print(
    "Folders:",
    report["folders"]
)

print(
    "Agents:",
    len(report["agents"])
)

print(
    "Engines:",
    len(report["engines"])
)

print(
    "Controllers:",
    len(report["controllers"])
)

print(
    "Brains:",
    len(report["brains"])
)

print("\nRecommendations:")

for r in report["recommendations"]:
    print("-", r)

print("\nSaved:")
print(
    "core/genesis/data/genesis_fusion_report.json"
)
