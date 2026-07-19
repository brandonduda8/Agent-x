from core.genesis.empire.empire_manager import (
    empire_manager
)


print("=" * 60)
print("👑 GENESIS EMPIRE MANAGER TEST")
print("=" * 60)


result = empire_manager.create_empire_cycle(
    "Healthcare AI Automation Company",
    "Healthcare AI"
)


print(result)

print(
    empire_manager.report()
)
