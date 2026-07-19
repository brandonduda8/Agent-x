from core.genesis.finance.financial_brain import (
    financial_brain
)


print("=" * 60)
print("🏦 GENESIS FINANCIAL INTELLIGENCE ENGINE TEST")
print("=" * 60)


result = financial_brain.analyze(
    "Healthcare AI Automation Company"
)


print(result)


print({
    "system":
    "GENESIS FINANCIAL INTELLIGENCE ENGINE v1",
    "cycles":
    len(financial_brain.cycles)
})
