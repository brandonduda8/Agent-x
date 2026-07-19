from core.genesis.master.genesis_master_orchestrator import (
    genesis_master_orchestrator
)


print("=" * 60)
print("👑 GENESIS MASTER ORCHESTRATOR TEST")
print("=" * 60)


result = genesis_master_orchestrator.execute(
    "Build a $100k/month AI automation company"
)


print(result)

print(
    genesis_master_orchestrator.report()
)
