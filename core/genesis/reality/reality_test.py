from core.genesis.reality.reality_engine import (
    reality_engine
)


print("=" * 60)
print("🌎 GENESIS REALITY EXECUTION ENGINE TEST")
print("=" * 60)


result = reality_engine.execute(
    "Acquire first AI automation customer",
    "Healthcare AI"
)


print(result)


print({
    "system": "GENESIS REALITY EXECUTION ENGINE v1",
    "cycles": len(reality_engine.cycles)
})
