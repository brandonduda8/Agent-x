import time

from core.genesis.agent_registry import agent_registry
from core.genesis.tool_registry import tool_registry
from core.genesis.executive_operating_system import executive_os


class GenesisExecutiveBootstrap:

    def __init__(self):
        self.system = "GENESIS EXECUTIVE BOOTSTRAP v1"
        self.loaded = False


    def load_agents(self):

        agents = [

            (
                "Agent-X",
                "Software Engineering Agent",
                [
                    "coding",
                    "automation",
                    "flutter",
                    "deployment"
                ]
            ),

            (
                "Hermes",
                "Coordination Agent",
                [
                    "planning",
                    "orchestration",
                    "MCP"
                ]
            ),

            (
                "Digital Twin",
                "Architecture Agent",
                [
                    "architecture",
                    "QA",
                    "research"
                ]
            ),

            (
                "Revenue Agent",
                "Business Growth Agent",
                [
                    "sales",
                    "lead_generation",
                    "automation"
                ]
            )

        ]


        results=[]

        for name, role, skills in agents:

            results.append(
                agent_registry.register(
                    name,
                    role,
                    skills
                )
            )

        return results



    def load_tools(self):

        tools=[

            (
                "Genesis API",
                "integration",
                "Connect Genesis services"
            ),

            (
                "Revenue Engine",
                "business",
                "Generate revenue workflows"
            ),

            (
                "MCP Mobile Bridge",
                "mobile",
                "Control mobile integrations"
            )

        ]


        results=[]

        for name, category, purpose in tools:

            results.append(

                tool_registry.register_tool(
                    name,
                    category,
                    purpose,
                    ["Genesis"]
                )

            )

        return results



    def boot(self):

        print(
            "🚀 Bootstrapping Genesis workforce..."
        )


        agents=self.load_agents()

        tools=self.load_tools()


        self.loaded=True


        return {

            "system":self.system,

            "agents_loaded":
                len(agents),

            "tools_loaded":
                len(tools),

            "status":
                "READY",

            "timestamp":
                time.time()

        }



bootstrap = GenesisExecutiveBootstrap()
