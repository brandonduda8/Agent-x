from genesis_core.adapters.adapter_registry import GenesisAdapterRegistry


def create_genesis_adapters():


    registry = GenesisAdapterRegistry()


    registry.register(

        "OpenRouter",

        "llm_provider",

        [

            "reasoning",

            "coding",

            "agent_models"

        ],

        "READY"

    )


    registry.register(

        "Telegram",

        "communication",

        [

            "commands",

            "notifications"

        ],

        "READY"

    )


    registry.register(

        "Stripe",

        "payments",

        [

            "payments",

            "revenue_tracking"

        ],

        "READY"

    )


    registry.register(

        "Agent-X",

        "agent_framework",

        [

            "coding",

            "deployment"

        ],

        "READY"

    )


    registry.register(

        "World Intelligence",

        "opportunity_source",

        [

            "jobs",

            "businesses",

            "markets"

        ],

        "READY"

    )


    return registry
