from core.genesis.portfolio_manager.portfolio_brain import (
    portfolio_brain
)


print("=" * 60)
print("🌐 GENESIS AUTONOMOUS PORTFOLIO MANAGER TEST")
print("=" * 60)


result = portfolio_brain.execute()


print(result)


print({
    "system":
    "GENESIS AUTONOMOUS PORTFOLIO MANAGER v1",
    "cycles":
    len(portfolio_brain.cycles)
})
