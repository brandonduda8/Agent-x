import time
import uuid


class GenesisAgentSelector:

    def __init__(self):

        self.system = "GENESIS AGENT SELECTOR v1"


    def select(self, task):

        print(
            f"🤖 Selecting agent for: {task}"
        )


        mapping = {

            "Research objective":
            "Research Agent",

            "Generate opportunities":
            "Lead Generation Agent",

            "Execute outreach":
            "Sales Agent",

            "Analyze results":
            "Analytics Agent",

            "Improve strategy":
            "Optimization Agent"

        }


        agent = mapping.get(
            task,
            "General Intelligence Agent"
        )


        return {

            "id":
            "agent_selection_" +
            uuid.uuid4().hex[:8],

            "task": task,

            "agent": agent,

            "status": "ASSIGNED",

            "timestamp": time.time()

        }


agent_selector = GenesisAgentSelector()
