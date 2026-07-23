import time


def register_live_source(payload=None):

    from core.genesis.genesis_live_source_manager import (
        genesis_live_source_manager
    )

    payload = payload or {}

    return genesis_live_source_manager.register_source(
        payload.get(
            "name",
            "Unknown Source"
        ),
        payload.get(
            "category",
            "UNKNOWN"
        ),
        payload.get(
            "connector"
        )
    )



def list_live_sources(payload=None):

    from core.genesis.genesis_live_source_manager import (
        genesis_live_source_manager
    )

    return genesis_live_source_manager.list_sources()



def sync_live_source(payload=None):

    from core.genesis.genesis_live_source_manager import (
        genesis_live_source_manager
    )

    payload = payload or {}

    return genesis_live_source_manager.sync_source(
        payload.get(
            "source_id"
        )
    )



def live_source_report(payload=None):

    from core.genesis.genesis_live_source_manager import (
        genesis_live_source_manager
    )

    return genesis_live_source_manager.report()



def register_live_source_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "register_live_source":
            register_live_source,

        "list_live_sources":
            list_live_sources,

        "sync_live_source":
            sync_live_source,

        "live_source_report":
            live_source_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
            "LIVE SOURCE MCP ONLINE",

        "tools":
            list(
                tools.keys()
            ),

        "timestamp":
            time.time()

    }
