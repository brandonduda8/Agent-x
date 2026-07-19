from core.genesis.permission_manager import permission_manager


permission_manager.register_agent(
    "Digital Twin",
    [
        "design_software",
        "create_projects",
        "use_ai_models",
        "request_mobile_access"
    ]
)


permission_manager.register_agent(
    "Agent-X",
    [
        "write_code",
        "use_github",
        "deploy_apps"
    ]
)


print(
    permission_manager.check(
        "Digital Twin",
        "create_projects"
    )
)


print(
    permission_manager.check(
        "Agent-X",
        "use_github"
    )
)


print(
    permission_manager.report()
)
