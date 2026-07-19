from core.genesis.developer_loop import developer_loop


cycle = developer_loop.start_cycle(
    "Genesis Mobile Command Center",
    "Build AI mobile workstation"
)


print(cycle)


print(
    developer_loop.complete_cycle(
        cycle["id"]
    )
)


print(
    developer_loop.report()
)
