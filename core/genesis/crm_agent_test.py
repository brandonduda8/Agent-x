from core.genesis.crm_agent import crm_agent


customer = crm_agent.create_customer(

    "Local Business",

    "Services",

    "Owner",

    "AI automation",

    0.88

)


print(customer)


print(
    crm_agent.update_stage(
        customer["id"],
        "QUALIFIED"
    )
)


print(
    crm_agent.add_activity(
        customer["id"],
        "AI automation consultation scheduled",
        "Sales Agent"
    )
)


print(
    crm_agent.status()
)
