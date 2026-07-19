from core.genesis.api_gateway import api_gateway


print(
    api_gateway.command(
        "Genesis find revenue opportunities"
    )
)


print(
    api_gateway.agents()
)


print(
    api_gateway.missions()
)


print(
    api_gateway.events()
)


print(
    api_gateway.approve(
        "Install Genesis mobile tools"
    )
)


print(
    api_gateway.status()
)
