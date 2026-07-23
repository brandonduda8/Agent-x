import time


def add_closer(payload=None):

    from core.genesis.sales_closer_network import (
        sales_closer_network
    )

    payload = payload or {}

    return sales_closer_network.add_closer(
        payload.get(
            "name",
            "Unknown Closer"
        ),
        payload.get(
            "skills",
            [
                "sales"
            ]
        ),
        payload.get(
            "experience",
            "unknown"
        )
    )



def match_closer(payload=None):

    from core.genesis.sales_closer_network import (
        sales_closer_network
    )

    payload = payload or {}

    return sales_closer_network.match_deal(
        payload.get(
            "opportunity",
            {}
        )
    )



def sales_closer_report(payload=None):

    from core.genesis.sales_closer_network import (
        sales_closer_network
    )

    return sales_closer_network.report()



def register_sales_closer_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "add_closer":
            add_closer,

        "match_closer":
            match_closer,

        "sales_closer_report":
            sales_closer_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
        "SALES CLOSER MCP ONLINE",

        "tools":
        list(
            genesis_mcp_server.tools.keys()
        ),

        "timestamp":
        time.time()

    }
