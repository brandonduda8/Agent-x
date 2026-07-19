from core.genesis.market.market_scanner import market_scanner
from core.genesis.market.opportunity_detector import opportunity_detector
from core.genesis.market.market_ranker import market_ranker
from core.genesis.market.business_generator import business_generator


print("=" * 60)
print("🧠 GENESIS MARKET INTELLIGENCE ENGINE TEST")
print("=" * 60)


scan = market_scanner.scan()

opportunities = []

for market in scan["markets"]:
    opportunities.append(
        opportunity_detector.evaluate(market)
    )


ranking = market_ranker.rank(opportunities)


best = ranking["ranking"][0]


company = business_generator.create(best)


print(company)

print(
    {
        "system": "GENESIS MARKET INTELLIGENCE ENGINE v1",
        "status": "COMPLETE"
    }
)
