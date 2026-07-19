from core.genesis.ceo_intelligence import GenesisCEOIntelligence
from core.genesis.agent_registry import agent_registry
from core.genesis.event_stream import event_stream


def main():

    agent_registry.register(
        "Revenue",
        "Business Growth",
        [
            "sales",
            "marketing"
        ]
    )

    agent_registry.register(
        "Researcher",
        "Market Research",
        [
            "analysis",
            "leads"
        ]
    )


    ceo = GenesisCEOIntelligence(
        agent_registry=agent_registry,
        event_stream=event_stream
    )


    result = ceo.analyze_objective(
        "Find AI automation customers"
    )


    print(result)

    print(
        ceo.report()
    )


if __name__ == "__main__":
    main()
