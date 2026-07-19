import time
import uuid

from core.genesis.execution.execution_tools import (
    execution_tools
)


class GenesisToolRegistry:

    def __init__(self):
        self.system = "GENESIS TOOL REGISTRY v1"
        self.tools = {}
        self.register_tools()


    def register_tools(self):

        self.tools = {
            "research": execution_tools.research_tool,
            "lead_generation": execution_tools.lead_generation_tool,
            "outreach": execution_tools.outreach_tool,
            "analytics": execution_tools.analytics_tool
        }


        print("🛠️ Genesis tools registered")


    def execute(self, tool, *args, **kwargs):

        print(f"⚡ Executing tool: {tool}")

        if tool not in self.tools:
            return {
                "error": "Tool unavailable"
            }

        result = self.tools[tool](
            *args,
            **kwargs
        )

        return result


    def report(self):

        return {
            "system": self.system,
            "tools": list(self.tools.keys()),
            "timestamp": time.time()
        }



tool_registry = GenesisToolRegistry()
