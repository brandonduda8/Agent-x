from core.genesis.llm_router import llm_router


llm_router.register_provider(
    "OpenRouter-NVIDIA",
    "NVIDIA AI Models",
    "OpenRouter"
)


llm_router.register_provider(
    "Gemini",
    "Gemini Advanced",
    "Google"
)


llm_router.connect_agent(
    "Agent-X",
    "OpenRouter-NVIDIA"
)


llm_router.connect_agent(
    "Digital Twin",
    "Gemini"
)


llm_router.connect_agent(
    "Hermes",
    "OpenRouter-NVIDIA"
)


llm_router.connect_agent(
    "OpenClaw",
    "Gemini"
)


print(
    llm_router.route(
        "Agent-X",
        "Build mobile application"
    )
)


print(
    llm_router.report()
)
