import json


from core.genesis.genesis_omega_evolution_core import (
    genesis_omega_evolution_core
)


evolution = genesis_omega_evolution_core


print(
    json.dumps(
        evolution.learn_pattern(
            "legal",
            "manual client intake",
            "AI intake automation",
            2500,
            "SUCCESS"
        ),
        indent=4
    )
)


print(
    json.dumps(
        evolution.score_agent(
            "Genesis AI Engineer Agent",
            True
        ),
        indent=4
    )
)


print(
    json.dumps(
        evolution.score_agent(
            "Genesis Software Engineer Agent",
            True
        ),
        indent=4
    )
)


print(
    json.dumps(
        evolution.generate_recommendation(),
        indent=4
    )
)


print(
    json.dumps(
        evolution.report(),
        indent=4
    )
)
