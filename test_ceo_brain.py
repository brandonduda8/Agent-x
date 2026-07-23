import json

from genesis_core.ceo.genesis_ceo_brain import (
    genesis_ceo_brain
)


opportunities = [

    {
        "name":
        "Dental AI Reception Automation",

        "category":
        "AI Automation",

        "value":
        999
    },


    {
        "name":
        "Remote AI Assistant Contract",

        "category":
        "employment",

        "value":
        1000
    }

]


agents = [

    "Hermes Research Agent",

    "Genesis Marketing Agent",

    "Agent-X Coding Agent"

]


decision = (
    genesis_ceo_brain.make_decision(
        opportunities,
        agents
    )
)


print(
    json.dumps(
        decision,
        indent=4
    )
)


print(
    json.dumps(
        genesis_ceo_brain.report(),
        indent=4
    )
)
