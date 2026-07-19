from core.genesis.workforce.workforce_manager import (
    workforce_manager
)


print("="*60)
print("👥 GENESIS WORKFORCE MANAGER TEST")
print("="*60)



result = workforce_manager.onboard(
    "Sales Agent",
    [
        "sales",
        "closing",
        "negotiation"
    ],
    95
)


print(result)


print(
    workforce_manager.report()
)
