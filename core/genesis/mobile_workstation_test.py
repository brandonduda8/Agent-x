from core.genesis.mobile_workstation import mobile_workstation


print(
    mobile_workstation.receive_command(
        "Genesis find revenue opportunities"
    )
)


print(
    mobile_workstation.send_to_agent(
        "Revenue Intelligence Agent",
        "Analyze fastest path to first customer"
    )
)


print(
    mobile_workstation.create_notification(
        "Genesis workstation online"
    )
)


print(
    mobile_workstation.report()
)
