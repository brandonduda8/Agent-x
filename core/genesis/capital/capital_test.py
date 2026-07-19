from core.genesis.capital.acquisition_engine import (
    acquisition_engine
)

from core.genesis.capital.valuation_engine import (
    valuation_engine
)

from core.genesis.capital.investment_engine import (
    investment_engine
)

from core.genesis.capital.merger_engine import (
    merger_engine
)


print("="*60)
print("🏦 GENESIS CAPITAL ENGINE TEST")
print("="*60)


target = acquisition_engine.scan(
    "Dental AI"
)


valuation = valuation_engine.evaluate(
    target
)


decision = investment_engine.decide(
    valuation
)


merger = merger_engine.merge(
    "Healthcare AI Automation Company",
    target["company"]
)


print(target)
print(valuation)
print(decision)
print(merger)


