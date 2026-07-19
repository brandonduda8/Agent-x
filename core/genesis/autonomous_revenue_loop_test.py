from core.genesis.autonomous_revenue_loop import autonomous_revenue_loop


cycle = autonomous_revenue_loop.start_cycle(

    "Acquire first 10 AI automation customers",

    "AI Automation Consulting Market",

    [
        "Growth Agent",
        "Revenue Agent",
        "Agent-X"
    ]

)


action = autonomous_revenue_loop.create_action(

    "Contact qualified local businesses",

    "Revenue Agent",

    1000

)


completed = autonomous_revenue_loop.complete_action(
    action["id"]
)


print(cycle)

print(action)

print(completed)

print(
    autonomous_revenue_loop.report()
)
