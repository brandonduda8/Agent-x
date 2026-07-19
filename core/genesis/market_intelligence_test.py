from core.genesis.market_intelligence_engine import (
    market_intelligence_engine
)


print("=" * 60)
print("🌎 GENESIS MARKET INTELLIGENCE ENGINE TEST")
print("=" * 60)


result = market_intelligence_engine.discover_opportunities(
    "AI automation companies",
    [
        "Healthcare AI Company",
        "Real Estate Automation Company",
        "Ecommerce AI Company"
    ]
)


print(result)

print(
    market_intelligence_engine.report()
)
