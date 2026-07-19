from core.genesis.software_factory import software_factory


project = software_factory.create_project(
    "Genesis Mobile Workstation",
    "Create Android AI command center"
)


print(project)


print(
    software_factory.update_status(
        project["id"],
        "BUILDING"
    )
)


print(
    software_factory.report()
)
