from core.genesis.workspace_manager import workspace_manager


workspace = workspace_manager.create_workspace(
    "Genesis Mobile Command Center",
    "Flutter Android Application",
    "Digital Twin"
)


print(workspace)


print(
    workspace_manager.add_file(
        workspace["id"],
        "main.dart",
        "Agent-X"
    )
)


print(
    workspace_manager.add_file(
        workspace["id"],
        "genesis_api.dart",
        "Agent-X"
    )
)


print(
    workspace_manager.list_workspaces()
)


print(
    workspace_manager.report()
)
