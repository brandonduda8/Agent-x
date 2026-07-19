from core.genesis.capability_graph import capability_graph


print(
    capability_graph.register_capability(
        "Revenue Automation",
        "business",
        [
            "sales",
            "lead_generation",
            "crm"
        ],
        "Revenue Agent"
    )
)


print(
    capability_graph.register_capability(
        "Software Development",
        "engineering",
        [
            "coding",
            "flutter",
            "deployment"
        ],
        "Agent-X"
    )
)


print(
    capability_graph.register_system(
        "Executive OS",
        "v1",
        "CEO decision management"
    )
)


print(
    capability_graph.find_capabilities(
        "sales"
    )
)


print(
    capability_graph.report()
)
