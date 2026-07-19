from core.genesis.command_router import command_router


print(
    command_router.process(
        "Genesis find revenue opportunities"
    )
)


print(
    command_router.process(
        "Genesis find online jobs"
    )
)


print(
    command_router.report()
)
