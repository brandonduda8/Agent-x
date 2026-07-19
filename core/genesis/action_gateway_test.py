from core.genesis.action_gateway import (
    action_gateway
)


print("=" * 50)
print("⚡ GENESIS ACTION GATEWAY TEST")
print("=" * 50)


def test_sales_tool(payload):

    return {
        "leads_found": 25,
        "message":
        "Lead research complete"
    }


action_gateway.register_tool(
    "Lead Research Tool",
    "lead_generation",
    test_sales_tool
)


result = action_gateway.execute_action(
    "Revenue Agent",
    "lead_generation",
    {
        "industry":
        "AI automation companies"
    }
)


print(result)


print(
    action_gateway.report()
)
