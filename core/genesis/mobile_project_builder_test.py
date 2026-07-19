from core.genesis.mobile_project_builder import mobile_project_builder


project = mobile_project_builder.create_project()


print(project)


print(
    mobile_project_builder.report()
)
