from core.genesis.mcp_mobile_bridge import mcp_mobile_bridge


mcp_mobile_bridge.register_tool(
    "device.status",
    "device",
    "termux-api"
)


mcp_mobile_bridge.register_tool(
    "notification.create",
    "events",
    "android-notifications"
)


mcp_mobile_bridge.register_tool(
    "workflow.trigger",
    "automation",
    "tasker"
)


print(
    mcp_mobile_bridge.discover_tools()
)


print(
    mcp_mobile_bridge.request_tool(
        "Hermes",
        "notification.create",
        {
            "message":
            "Genesis MCP Bridge online"
        }
    )
)


print(
    mcp_mobile_bridge.status()
)
