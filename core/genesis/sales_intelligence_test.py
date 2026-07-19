from core.genesis.sales_intelligence_engine import (
    sales_intelligence_engine
)


print("=" * 60)
print("🧠 GENESIS SALES INTELLIGENCE ENGINE TEST")
print("=" * 60)


opportunity = {
    "company": "Healthcare AI Company",
    "score": 90
}


result = sales_intelligence_engine.process_opportunity(
    opportunity
)


print(result)

print(
    sales_intelligence_engine.report()
)
