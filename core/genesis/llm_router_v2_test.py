from core.genesis.llm_router_v2 import llm_router_v2


llm_router_v2.register_provider(
    "Kimi",
    "kimi-k2.6",
    [
        "coding",
        "agents",
        "reasoning",
        "long_context"
    ]
)


llm_router_v2.register_provider(
    "Gemini",
    "Gemini Advanced",
    [
        "multimodal",
        "research"
    ]
)


llm_router_v2.connect_agent(
    "Agent-X",
    "Kimi"
)


llm_router_v2.connect_agent(
    "Digital Twin",
    "Gemini"
)


print(
    llm_router_v2.route_task(
        "Agent-X",
        "Build Genesis CRM system"
    )
)


print(
    llm_router_v2.status()
)
