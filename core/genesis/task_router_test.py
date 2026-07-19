from core.genesis.task_router import task_router


print(
    task_router.route_mission(
        "Find fastest path to first revenue client"
    )
)


print(
    task_router.report()
)
