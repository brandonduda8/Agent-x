from core.genesis.agent_heartbeat_system import agent_heartbeat_system


agent_heartbeat_system.register_agent(

    "Agent-X",

    "Software Engineer",

    [
        "coding",
        "automation",
        "deployment"
    ]

)


agent_heartbeat_system.register_agent(

    "Revenue Agent",

    "Sales Intelligence",

    [
        "sales",
        "crm",
        "lead_generation"
    ]

)


heartbeat = agent_heartbeat_system.heartbeat(

    "Agent-X",

    "Build customer acquisition system",

    "Create automation platform"

)


agent_heartbeat_system.heartbeat(

    "Revenue Agent",

    "Acquire first AI automation customers",

    "Generate qualified leads"

)


agent_heartbeat_system.update_health(

    "Agent-X",

    98

)


print(heartbeat)

print(
    agent_heartbeat_system.workforce_status()
)
