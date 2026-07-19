from core.genesis.autonomous_developer_pipeline import autonomous_developer_pipeline


build = autonomous_developer_pipeline.create_build(
    "Genesis Mobile Command Center",
    "Create Android AI workstation"
)


print(build)


print(
    autonomous_developer_pipeline.execute_build(
        build["id"]
    )
)


print(
    autonomous_developer_pipeline.report()
)
