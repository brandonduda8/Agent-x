from core.genesis.genesis_reality_action_executor import action_executor


actions = [

    (
        "income",
        "Identify and rank immediate employment opportunities",
        "Opportunity Discovery Agent",
        "CRITICAL"
    ),

    (
        "income",
        "Prepare first application batch",
        "Outreach Agent",
        "CRITICAL"
    ),

    (
        "revenue",
        "Create AI automation service offer",
        "Revenue Agent",
        "HIGH"
    ),

    (
        "revenue",
        "Build business lead pipeline",
        "Revenue Agent",
        "HIGH"
    ),

    (
        "housing",
        "Collect housing assistance contacts",
        "Stability Agent",
        "CRITICAL"
    ),

    (
        "execution",
        "Review progress and adjust strategy",
        "Zane Hart Agent",
        "HIGH"
    )

]


for item in actions:

    print(
        action_executor.create_action(
            item[0],
            item[1],
            item[2],
            item[3]
        )
    )


print(action_executor.status())
