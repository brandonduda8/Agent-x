import time
import uuid


class AgentFactory:

    def __init__(self):
        self.system = "GENESIS META AGENT FACTORY v1"
        self.agents = []

    def create(self, capability):

        agent = {
            "id": "meta_agent_" + uuid.uuid4().hex[:8],
            "name": capability + " Specialist",
            "skills": [capability],
            "status": "CREATED",
            "created": time.time()
        }

        self.agents.append(agent)

        print(f"🏗️ New meta agent created: {agent['name']}")

        return agent


agent_factory = AgentFactory()
