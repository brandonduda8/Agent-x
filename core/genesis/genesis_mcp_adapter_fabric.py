import time
import uuid

from core.genesis.tool_registry import tool_registry


class GenesisMCPAdapterFabric:
    """
    GENESIS MCP ADAPTER FABRIC v1

    Purpose:
    - Discover MCP capability adapters
    - Convert adapters into Genesis tools
    - Connect agent capabilities to tool registry
    - Provide unified MCP capability layer

    Flow:

    MCP ADAPTERS
          |
          v
    MCP ADAPTER FABRIC
          |
          v
    GENESIS TOOL REGISTRY
          |
          v
    AGENT WORKFORCE
    """

    def __init__(self):
        self.system = "GENESIS MCP ADAPTER FABRIC v1"

        self.adapters = {}
        self.history = []


    def register_adapter(
        self,
        name,
        category,
        capabilities
    ):
        adapter = {
            "id": "adapter_" + uuid.uuid4().hex[:8],
            "name": name,
            "category": category,
            "capabilities": capabilities,
            "status": "ACTIVE",
            "created": time.time()
        }

        self.adapters[name] = adapter

        return adapter


    def discover_tools(self):
        """
        Initial Genesis capability discovery.

        External MCP servers can be attached later.
        """

        tools = [

            (
                "research_adapter",
                "research",
                [
                    "web research",
                    "market analysis",
                    "competitor research"
                ]
            ),

            (
                "revenue_adapter",
                "revenue",
                [
                    "lead generation",
                    "sales",
                    "outreach",
                    "offers"
                ]
            ),

            (
                "engineering_adapter",
                "engineering",
                [
                    "coding",
                    "debugging",
                    "testing",
                    "deployment"
                ]
            ),

            (
                "memory_adapter",
                "memory",
                [
                    "knowledge storage",
                    "learning",
                    "history"
                ]
            )
        ]


        registered = []

        for name, category, capabilities in tools:

            adapter = self.register_adapter(
                name,
                category,
                capabilities
            )

            registered.append(adapter)


        return registered



    def sync_tool_registry(self):
        """
        Converts MCP adapters into Genesis tools.
        """

        synced = []


        for name, adapter in self.adapters.items():

            try:

                tool_registry.register_tool(
                    name=name,
                    category=adapter["category"],
                    purpose=(
                        "MCP capability adapter for "
                        + adapter["category"]
                        + " operations"
                    ),
                    agents=adapter.get(
                        "capabilities",
                        []
                    )
                )


                synced.append(name)


            except Exception as e:

                print(
                    f"⚠️ Tool sync failed {name}: {e}"
                )


        return synced



    def map_agent_capabilities(self):

        agents = [

            "Genesis Computer Science Architect Agent",
            "Genesis Software Engineer Agent",
            "Genesis AI Engineer Agent",
            "Genesis QA Scientist Agent",
            "Genesis Knowledge Engineer Agent"

        ]


        capabilities = [

            "web research",
            "market analysis",
            "competitor research",
            "lead generation",
            "sales",
            "outreach",
            "offers",
            "coding",
            "debugging",
            "testing",
            "deployment",
            "knowledge storage",
            "learning",
            "history"

        ]


        return {
            agent: capabilities
            for agent in agents
        }



    def activate(self):

        print(
            "\n🔌 GENESIS MCP ADAPTER FABRIC"
        )


        adapters = self.discover_tools()


        tools = self.sync_tool_registry()


        mapping = self.map_agent_capabilities()


        report = {

            "system": self.system,

            "status": "ONLINE",

            "adapters": len(adapters),

            "tools_connected": len(tools),

            "agent_capability_map": mapping,

            "timestamp": time.time()

        }


        self.history.append(report)


        print(
            "✅ MCP adapters activated"
        )


        return report



    def report(self):

        return {

            "system": self.system,

            "adapters": len(self.adapters),

            "history": len(self.history),

            "timestamp": time.time()

        }



genesis_mcp_adapter_fabric = GenesisMCPAdapterFabric()
