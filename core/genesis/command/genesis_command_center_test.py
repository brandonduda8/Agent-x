from core.genesis.command.genesis_command_center import (
    genesis_command_center
)


print("=" * 60)
print("🧠 GENESIS COMMAND CENTER TEST")
print("=" * 60)


result = genesis_command_center.run(
    "Acquire first AI automation customers",
    "Healthcare AI"
)


print(result)

print(
    genesis_command_center.report()
)
