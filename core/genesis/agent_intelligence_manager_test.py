from core.genesis.agent_intelligence_manager import agent_intelligence_manager


print(
    agent_intelligence_manager.create_agent(
        "Mobile Development Agent",
        "Build Genesis mobile applications",
        [
            "Flutter",
            "React Native",
            "Termux API"
        ],
        [
            "create_apps",
            "manage_projects",
            "request_device_access"
        ],
        "OpenRouter-NVIDIA"
    )
)


print(
    agent_intelligence_manager.create_agent(
        "Revenue Intelligence Agent",
        "Find and evaluate revenue opportunities",
        [
            "Web Research",
            "Marketing Engine",
            "Lead Database"
        ],
        [
            "analyze_markets",
            "create_campaigns"
        ],
        "Gemini"
    )
)


print(
    agent_intelligence_manager.report()
)
