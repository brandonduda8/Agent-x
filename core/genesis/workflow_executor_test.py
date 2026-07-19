from core.genesis.task_router import task_router
from core.genesis.workflow_executor import workflow_executor


tasks = task_router.route_mission(
    "Find fastest path to first revenue client"
)


print(
    workflow_executor.execute(tasks)
)


print(
    workflow_executor.report()
)
