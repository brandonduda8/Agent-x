from core.genesis.software_factory import software_factory
from core.genesis.development_pipeline import development_pipeline


project = software_factory.create_project(
    "Genesis Mobile Workstation",
    "Create Android AI command center"
)


build = development_pipeline.start_build(
    project
)


print(build)


for task in project["tasks"]:

    print(
        development_pipeline.run_task(
            build["id"],
            task["task"]
        )
    )


print(
    development_pipeline.complete_build(
        build["id"]
    )
)


print(
    development_pipeline.report()
)
