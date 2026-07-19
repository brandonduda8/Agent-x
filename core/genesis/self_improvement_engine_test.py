from core.genesis.self_improvement_engine import self_improvement_engine


execution = {

    "mission":
        "Find and close first AI automation customer",

    "results":

    [

        {
            "agent":
                "Agent-X",

            "result":
                "SUCCESS"
        },

        {
            "agent":
                "Revenue Agent",

            "result":
                "SUCCESS"
        },

        {
            "agent":
                "CRM Agent",

            "result":
                "SUCCESS"
        }

    ]

}



learning = self_improvement_engine.analyze_execution(
    execution
)


upgrade = self_improvement_engine.create_upgrade(
    "Revenue Agent",
    "Improve customer outreach intelligence"
)


print(learning)

print(upgrade)

print(
    self_improvement_engine.report()
)
