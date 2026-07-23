import time


def scan_money(payload=None):

    from core.genesis.internet_job_connector import (
        internet_job_connector
    )

    from core.genesis.revenue_execution_engine import (
        revenue_execution_engine
    )


    opportunities = (
        internet_job_connector
        .scan()
        ["jobs"]
    )


    return revenue_execution_engine.analyze(
        opportunities
    )



def revenue_execution_report(payload=None):

    from core.genesis.revenue_execution_engine import (
        revenue_execution_engine
    )

    return revenue_execution_engine.report()



def register_revenue_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "scan_money":
            scan_money,

        "revenue_execution_report":
            revenue_execution_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
            "REVENUE EXECUTION MCP ONLINE",

        "tools":
            list(
                tools.keys()
            ),

        "timestamp":
            time.time()

    }
