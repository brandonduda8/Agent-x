import json


from genesis_core.revenue.revenue_activation_bridge import (
    genesis_revenue_activation_bridge
)


execution = {

    "id":
    "execution_demo",

    "mission":
    "Dental AI Reception Automation"

}


activation = (
    genesis_revenue_activation_bridge.activate(
        execution
    )
)


print(
    json.dumps(
        activation,
        indent=4
    )
)


print(
    json.dumps(
        genesis_revenue_activation_bridge.report(),
        indent=4
    )
)
