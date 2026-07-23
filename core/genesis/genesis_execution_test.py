from core.genesis.genesis_bootstrap import genesis_command_center
from core.genesis.genesis_execution_orchestrator import (
    GenesisExecutionOrchestrator
)

from core.genesis.revenue_execution_engine import (
    GenesisRevenueExecutionEngine
)

from core.genesis.developer_loop import developer_loop
from core.genesis.genesis_memory import genesis_memory


mission = genesis_command_center.submit_goal(
    "Create an AI automation service to generate revenue"
)


orchestrator = GenesisExecutionOrchestrator(
    revenue_execution_engine=GenesisRevenueExecutionEngine(),
    developer_loop=developer_loop,
    genesis_memory=genesis_memory
)


result = orchestrator.execute(
    mission
)


print("\nEXECUTION RESULT")
print(result)


print("\nORCHESTRATOR REPORT")
print(orchestrator.report())
