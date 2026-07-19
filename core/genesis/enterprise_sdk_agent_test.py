from core.genesis.enterprise_sdk_agent import enterprise_sdk_agent


sdk = enterprise_sdk_agent.register_sdk(

    "Stripe API",

    "Payments",

    "Process customer payments",

    "API Key"

)


print(sdk)


print(
    enterprise_sdk_agent.design_connector(
        sdk["id"],
        "Revenue Agent"
    )
)


print(
    enterprise_sdk_agent.status()
)
