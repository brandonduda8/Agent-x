from core.genesis.device_bridge import device_bridge


print(
    device_bridge.notify(
        "Genesis device bridge online"
    )
)


print(
    device_bridge.execute_allowed_action(
        "check_status"
    )
)


print(
    device_bridge.execute_allowed_action(
        "install_everything"
    )
)


print(
    device_bridge.report()
)
