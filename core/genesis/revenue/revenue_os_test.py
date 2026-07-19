from core.genesis.revenue.revenue_orchestrator import (
    revenue_orchestrator
)


print("=" * 60)
print("💰 GENESIS REVENUE OPERATING SYSTEM TEST")
print("=" * 60)


result = revenue_orchestrator.run(
    "Healthcare AI"
)


print(result)
