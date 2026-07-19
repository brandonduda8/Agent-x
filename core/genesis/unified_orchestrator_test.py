from core.genesis.unified_orchestrator import unified_orchestrator


execution = unified_orchestrator.execute_objective(
    "Find fastest path to first revenue"
)


print(execution)


print(
    unified_orchestrator.complete_execution(
        execution["id"]
    )
)


print(
    unified_orchestrator.report()
)
