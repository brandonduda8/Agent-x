from core.genesis.sales_force.sales_manager import (
    sales_manager
)


print("=" * 60)
print("🤖 GENESIS AUTONOMOUS SALES FORCE TEST")
print("=" * 60)


result = sales_manager.execute(
    "Healthcare AI"
)


print(result)


print({
    "system": "GENESIS AUTONOMOUS SALES FORCE v1",
    "cycles": len(sales_manager.cycles)
})
