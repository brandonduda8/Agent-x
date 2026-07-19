from core.genesis.autonomous_revenue_loop_controller import (
    autonomous_revenue_loop_controller
)


print("=" * 60)
print("👑 GENESIS AUTONOMOUS REVENUE LOOP TEST")
print("=" * 60)


result = (
    autonomous_revenue_loop_controller
    .start_cycle(
        "Acquire first AI automation customers"
    )
)


print(result)

print(
    autonomous_revenue_loop_controller.report()
)
