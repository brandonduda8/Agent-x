from core.genesis.revenue_acquisition_engine import (
    revenue_acquisition_engine
)


print("=" * 60)
print("💰 GENESIS REVENUE ACQUISITION ENGINE TEST")
print("=" * 60)


result = revenue_acquisition_engine.run(
    "Acquire first AI automation customers",
    "AI automation companies",
    "AI automation consulting and implementation package"
)


print(result)

print(
    revenue_acquisition_engine.report()
)
