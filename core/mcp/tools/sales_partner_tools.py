import time


def add_sales_partner(payload=None):

    from core.genesis.sales_partner_agent import (
        sales_partner_agent
    )

    payload = payload or {}

    return sales_partner_agent.add_partner(
        payload.get(
            "name",
            "Unknown Partner"
        ),
        payload.get(
            "contact",
            "unknown"
        ),
        payload.get(
            "skills",
            [
                "sales",
                "closing",
                "AI services"
            ]
        ),
        payload.get(
            "commission",
            50
        )
    )



def create_commission_offer(payload=None):

    from core.genesis.sales_partner_agent import (
        sales_partner_agent
    )

    payload = payload or {}

    return sales_partner_agent.create_commission_offer(
        payload.get(
            "opportunity",
            {}
        ),
        payload.get(
            "commission",
            50
        )
    )



def match_deal_to_partner(payload=None):

    from core.genesis.sales_partner_agent import (
        sales_partner_agent
    )

    payload = payload or {}

    return sales_partner_agent.match_partner(
        payload.get(
            "opportunity",
            {}
        )
    )



def sales_partner_report(payload=None):

    from core.genesis.sales_partner_agent import (
        sales_partner_agent
    )

    return sales_partner_agent.report()



def register_sales_partner_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "add_sales_partner":
            add_sales_partner,

        "create_commission_offer":
            create_commission_offer,

        "match_deal_to_partner":
            match_deal_to_partner,

        "sales_partner_report":
            sales_partner_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
            "SALES PARTNER MCP ONLINE",

        "tools":
            list(
                tools.keys()
            ),

        "timestamp":
            time.time()

    }
