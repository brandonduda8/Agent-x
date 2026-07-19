from core.genesis.identity_core import identity_core


print(
    identity_core.register_agent(
        "Agent-X",
        "Software Engineer",
        [
            "coding",
            "automation",
            "flutter"
        ]
    )
)


print(
    identity_core.register_agent(
        "Hermes",
        "Coordinator",
        [
            "planning",
            "MCP",
            "orchestration"
        ]
    )
)


print(
    identity_core.register_tool(
        "Genesis API",
        "integration",
        "Connect Genesis services"
    )
)


print(
    identity_core.record_upgrade(
        "Executive OS Integration",
        "v1"
    )
)


print(
    identity_core.report()
)
