from core.genesis.capital_allocation.investment_brain import (
    investment_brain
)


print("=" * 60)
print("🏛️ GENESIS CAPITAL ALLOCATION ENGINE TEST")
print("=" * 60)


result = investment_brain.execute(
    "Healthcare AI Automation Company"
)


print(result)


print({
    "system":
    "GENESIS CAPITAL ALLOCATION ENGINE v1",
    "cycles":
    len(investment_brain.cycles)
})
