import time


def scan_money_missions(payload=None):

    from core.genesis.money_mission_router import (
        money_mission_router
    )

    payload = payload or {}

    opportunities = payload.get(
        "opportunities",
        []
    )

    return money_mission_router.scan(
        opportunities
    )



def money_mission_report(payload=None):

    from core.genesis.money_mission_router import (
        money_mission_router
    )

    return money_mission_router.report()



def register_money_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "scan_money_missions":
            scan_money_missions,

        "money_mission_report":
            money_mission_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
            "MONEY MISSION MCP ONLINE",

        "tools":
            list(
                tools.keys()
            ),

        "timestamp":
            time.time()

    }
