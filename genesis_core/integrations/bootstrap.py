from genesis_core.integrations.orchestrator import GenesisIntegrationOrchestrator



def build_integrations():

    system = GenesisIntegrationOrchestrator()


    system.register_adapter(

        "OpenRouter",

        "LLM Provider",

        [

        "reasoning",

        "coding",

        "agent_models"

        ]

    )


    system.register_adapter(

        "Telegram",

        "Communication",

        [

        "commands",

        "notifications"

        ]

    )


    system.register_adapter(

        "Stripe",

        "Payments",

        [

        "revenue_tracking",

        "payments"

        ]

    )


    system.register_adapter(

        "Agent-X",

        "Agent Framework",

        [

        "coding",

        "deployment"

        ]

    )


    system.register_adapter(

        "Hermes/OpenClaw",

        "Agent Workers",

        [

        "research",

        "execution"

        ]

    )


    system.register_adapter(

        "STEM Meta Agents",

        "Knowledge",

        [

        "science",

        "engineering",

        "learning"

        ]

    )


    system.register_adapter(

        "World Intelligence",

        "Opportunity Source",

        [

        "jobs",

        "business",

        "markets"

        ]

    )


    return system
