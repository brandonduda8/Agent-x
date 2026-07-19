from core.genesis.mobile_api_server import mobile_api_server


print(
    mobile_api_server.receive_command(
        "Genesis find revenue opportunities"
    )
)


print(
    mobile_api_server.get_agents()
)


print(
    mobile_api_server.get_missions()
)


print(
    mobile_api_server.approve_action(
        "Send customer outreach"
    )
)


print(
    mobile_api_server.report()
)
