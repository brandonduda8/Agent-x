import json


from core.genesis.genesis_long_term_memory import (
    genesis_long_term_memory
)


print(
    genesis_long_term_memory.store_pattern(
        "legal",
        "manual client intake",
        "AI intake automation",
        2500,
        "SUCCESS"
    )
)


print(
    genesis_long_term_memory.store_agent(
        "Genesis AI Engineer Agent",
        True,
        1.0
    )
)


print(
    genesis_long_term_memory.store_revenue(
        2500,
        "Legal AI Automation Package"
    )
)


print(
    json.dumps(
        genesis_long_term_memory.report(),
        indent=4
    )
)
