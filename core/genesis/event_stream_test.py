from core.genesis.event_stream import event_stream


print(
    event_stream.subscribe(
        "Genesis Mobile App"
    )
)


print(
    event_stream.emit(
        "AGENT_COMPLETED_TASK",
        "Agent-X",
        {
            "task":
            "Build mobile dashboard"
        }
    )
)


print(
    event_stream.emit(
        "REVENUE_OPPORTUNITY_FOUND",
        "Revenue Intelligence Agent",
        {
            "opportunity":
            "AI automation service"
        }
    )
)


print(
    event_stream.latest()
)


print(
    event_stream.report()
)
