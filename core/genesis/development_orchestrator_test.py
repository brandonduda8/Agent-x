from core.genesis.development_orchestrator import development_orchestrator


project = development_orchestrator.create_project(
    "Genesis Mobile Workstation",
    "Create a mobile AI command center for Genesis agents"
)


print(project)


development_orchestrator.start_project(
    project["id"]
)


print(
    development_orchestrator.report()
)
