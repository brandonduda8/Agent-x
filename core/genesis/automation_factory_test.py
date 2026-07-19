from core.genesis.automation_factory import automation_factory


automation = automation_factory.create_automation(

    "Genesis Revenue Alert",

    "Revenue opportunity discovered",

    "Create mobile notification and assign outreach task",

    "Revenue Intelligence Agent",

    "Genesis Notification Assistant"

)


print(automation)


print(
    automation_factory.activate(
        automation["id"]
    )
)


print(
    automation_factory.list_automations()
)


print(
    automation_factory.status()
)
