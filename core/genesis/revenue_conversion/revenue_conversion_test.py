from core.genesis.revenue_conversion.revenue_conversion_engine import (
    revenue_conversion_engine
)


print("=" * 60)
print("💰 GENESIS REVENUE CONVERSION ENGINE TEST")
print("=" * 60)


result = revenue_conversion_engine.execute(
    "Healthcare AI Company 1"
)


print(result)


print({
    "system": "GENESIS REVENUE CONVERSION ENGINE v1",
    "cycles": len(revenue_conversion_engine.cycles)
})
