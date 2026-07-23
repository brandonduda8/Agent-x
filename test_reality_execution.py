import json


from genesis_core.execution.genesis_reality_execution_engine import (
    genesis_reality_execution_engine
)


mission = {

    "opportunity":
    "Dental AI Reception Automation",

    "agents":
    [
        "Hermes Research Agent",
        "Genesis Marketing Agent",
        "Agent-X Coding Agent"
    ],

    "actions":
    [
        "Research dental businesses",
        "Create client outreach",
        "Build automation demo"
    ]

}


execution = (
    genesis_reality_execution_engine.execute_mission(
        mission
    )
)


print(
    json.dumps(
        execution,
        indent=4
    )
)


print(
    json.dumps(
        genesis_reality_execution_engine.report(),
        indent=4
    )
)
