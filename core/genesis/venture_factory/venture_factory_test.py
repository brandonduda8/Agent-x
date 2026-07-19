from core.genesis.venture_factory.venture_factory import (
    venture_factory
)


print("="*60)
print("🏭 GENESIS VENTURE FACTORY TEST")
print("="*60)


opportunity = {
    "market":"Healthcare AI",
    "score":92
}


result = venture_factory.create(
    opportunity
)


print(result)


print({
    "system": venture_factory.system,
    "ventures": len(venture_factory.ventures)
})
