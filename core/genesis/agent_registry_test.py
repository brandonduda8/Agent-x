from core.genesis.agent_registry import agent_registry


agent_registry.register(
    "Agent-X",
    "Autonomous builder and automation engineer",
    [
        "coding",
        "deployment",
        "system building",
        "automation"
    ],
    "LOCAL"
)


agent_registry.register(
    "Digital Twin",
    "Personal AI operating assistant",
    [
        "planning",
        "memory",
        "personal workflows",
        "decision support"
    ],
    "LOCAL"
)


agent_registry.register(
    "Hermes",
    "Task execution and agent coordination system",
    [
        "orchestration",
        "task routing",
        "agent communication"
    ],
    "LOCAL"
)


agent_registry.register(
    "OpenClaw",
    "External agent framework connector",
    [
        "agent tools",
        "extensions",
        "automation"
    ],
    "LOCAL"
)


print(agent_registry.report())
