from core.genesis.autonomous_flutter_builder import autonomous_flutter_builder


build = autonomous_flutter_builder.create_flutter_build(
    "Genesis Mobile Command Center"
)


print(build)


print(
    autonomous_flutter_builder.complete_build(
        build["id"]
    )
)


print(
    autonomous_flutter_builder.report()
)
