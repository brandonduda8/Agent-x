from core.genesis.mobile_integration_layer import mobile_integration_layer


print(
    mobile_integration_layer.connect_device(
        "Android Genesis Workstation"
    )
)


print(
    mobile_integration_layer.send_command(
        "Genesis find revenue opportunities"
    )
)


print(
    mobile_integration_layer.receive_event(
        "AGENT_RESPONSE",
        {
            "agent": "Digital Twin",
            "message": "Revenue analysis complete"
        }
    )
)


print(
    mobile_integration_layer.get_status()
)
