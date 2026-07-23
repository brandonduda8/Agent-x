import json


from core.genesis.genesis_strategy_engine import (
    genesis_strategy_engine
)


pattern = {

    "industry":
        "legal",

    "problem":
        "manual client intake",

    "solution":
        "AI intake automation",

    "revenue":
        2500,

    "result":
        "SUCCESS"

}



strategy = (
    genesis_strategy_engine.analyze_pattern(
        pattern
    )
)


print(
    json.dumps(
        strategy,
        indent=4
    )
)


mission = (
    genesis_strategy_engine.create_mission(
        strategy
    )
)


print(
    json.dumps(
        mission,
        indent=4
    )
)


print(
    json.dumps(
        genesis_strategy_engine.report(),
        indent=4
    )
)
