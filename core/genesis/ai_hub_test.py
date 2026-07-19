from core.genesis.ai_communication_hub import ai_hub


ai_hub.register_provider(
    "OpenRouter-NVIDIA",
    "NVIDIA hosted LLM"
)


ai_hub.register_provider(
    "Gemini",
    "Google Gemini"
)


print(
    ai_hub.broadcast(
        "Find opportunities to create revenue this week"
    )
)


print(
    ai_hub.report()
)
