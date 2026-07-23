import json


from genesis_core.fusion.revenue_fusion_adapter import (
    genesis_revenue_fusion_adapter
)



mission = (
    genesis_revenue_fusion_adapter.activate_offer(
        "Bright Smile Dental",
        "Dental",
        "Missed calls and lost appointments",
        "AI Reception Automation System",
        999
    )
)


print(
    json.dumps(
        mission,
        indent=4,
        default=str
    )
)


print(
    json.dumps(
        genesis_revenue_fusion_adapter.dashboard(),
        indent=4,
        default=str
    )
)
