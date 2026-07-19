from core.genesis.operations.agent_health_monitor import (
    agent_health_monitor
)


print("=" * 60)
print("❤️ GENESIS AGENT HEALTH SYSTEM TEST")
print("=" * 60)


agent_health_monitor.register_agent(
    "Sales Agent",
    [
        "sales",
        "crm",
        "lead_generation"
    ]
)


agent_health_monitor.heartbeat(
    "Sales Agent"
)


agent_health_monitor.record_task(
    "Sales Agent",
    True,
    5000
)


agent_health_monitor.record_task(
    "Sales Agent",
    True,
    2500
)


analysis = agent_health_monitor.analyze_agent(
    "Sales Agent"
)


print(analysis)

print(
    agent_health_monitor.report()
)
