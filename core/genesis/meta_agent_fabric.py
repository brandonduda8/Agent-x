import time
import os


class MetaAgentFabric:

    def __init__(self):

        self.agents = [

            {
                "name": "Agent-X",
                "type": "general_agent_execution",
                "adapter": "core/genesis/agent_x_bridge.py",
                "status": self.check(
                    "core/genesis/agent_x_bridge.py"
                )
            },

            {
                "name": "Zane Hart Agent",
                "type": "advanced_reasoning_meta_agent",
                "adapter": "AGENT_X_COMPATIBILITY_LAYER",
                "status": "REGISTERED"
            },

            {
                "name": "STEM Meta Agent",
                "type": "science_technology_engineering_math",
                "adapter": "agents/meta_auditor.py",
                "status": self.check(
                    "agents/meta_auditor.py"
                )
            },

            {
                "name": "Computer Science Meta Agent",
                "type": "software_architecture_and_engineering",
                "adapter": "agents/builder/builder_agent.py",
                "status": self.check(
                    "agents/builder/builder_agent.py"
                )
            },

            {
                "name": "Research Meta Agent",
                "type": "knowledge_discovery",
                "adapter": "agents/researcher/researcher_agent.py",
                "status": self.check(
                    "agents/researcher/researcher_agent.py"
                )
            },

            {
                "name": "Planning Meta Agent",
                "type": "strategy_and_execution_planning",
                "adapter": "agents/planner/planner_agent.py",
                "status": self.check(
                    "agents/planner/planner_agent.py"
                )
            }
        ]


    def check(self, path):

        if os.path.exists(path):
            return "ADAPTER_FOUND"

        return "MISSING"


    def status(self):

        return {
            "system": "GENESIS META AGENT FABRIC v1",
            "status": "ONLINE",
            "agents": self.agents,
            "timestamp": time.time()
        }


meta_agent_fabric = MetaAgentFabric()
