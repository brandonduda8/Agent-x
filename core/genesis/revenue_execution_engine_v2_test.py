from core.genesis.revenue_execution_engine_v2 import (
    revenue_execution_engine_v2
)


print("=" * 60)
print("💰 GENESIS REVENUE EXECUTION ENGINE v2 TEST")
print("=" * 60)


result = revenue_execution_engine_v2.execute(
    "Healthcare AI Company"
)


print(result)

print(
    revenue_execution_engine_v2.report()
)
