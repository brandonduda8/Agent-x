import json

from genesis_core.ceo.genesis_autonomous_ceo_loop import (
    genesis_autonomous_ceo_loop
)


cycle = (
    genesis_autonomous_ceo_loop.run_cycle()
)


print(
    json.dumps(
        cycle,
        indent=4
    )
)


print(
    json.dumps(
        genesis_autonomous_ceo_loop.report(),
        indent=4
    )
)
