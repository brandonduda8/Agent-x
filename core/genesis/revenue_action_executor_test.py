from core.genesis.revenue_execution_engine_v2 import (
    revenue_execution_engine_v2
)

from core.genesis.revenue_action_executor import (
    revenue_action_executor
)


print("=" * 60)
print("⚡ GENESIS REVENUE ACTION EXECUTOR TEST")
print("=" * 60)


execution = revenue_execution_engine_v2.execute(
    "Healthcare AI Company"
)


result = revenue_action_executor.run(
    execution["opportunity"],
    execution["sales_action"]
)


print(result)

print(
    revenue_action_executor.report()
)
