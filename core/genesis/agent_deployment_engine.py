import time
import uuid

from core.genesis.worker_registry import worker_registry
from core.genesis.workforce_memory import workforce_memory


class AgentDeploymentEngine:

    def __init__(self):

        self.system = "GENESIS AGENT DEPLOYMENT ENGINE v2.1"
        self.deployments = []


    def deploy(self, agent):

        worker = {

            "id":
                agent.get(
                    "id",
                    "worker_" + uuid.uuid4().hex[:8]
                ),

            "name":
                agent.get(
                    "name",
                    "Unknown Agent"
                ),

            "capability":
                agent.get(
                    "role",
                    "unknown"
                ),

            "skills":
                agent.get(
                    "skills",
                    []
                ),

            "missions":
                0,

            "performance":
                100,

            "status":
                "ONLINE"

        }


        worker_registry.register(
            worker
        )


        workforce_memory.add_worker(
            worker
        )


        deployment = {

            "id":
                "deployment_" + uuid.uuid4().hex[:8],

            "agent":
                worker["name"],

            "role":
                worker["capability"],

            "skills":
                worker["skills"],

            "status":
                "ONLINE",

            "created":
                time.time()

        }


        self.deployments.append(
            deployment
        )


        print(
            "🧬 Worker Registered:",
            worker["name"]
        )

        print(
            "💾 Worker Saved To Memory"
        )

        print(
            "🚀 Agent Deployed:",
            worker["name"]
        )


        return deployment



    def report(self):

        return {

            "system":
                self.system,

            "deployments":
                len(
                    self.deployments
                ),

            "memory":
                workforce_memory.report(),

            "timestamp":
                time.time()

        }



agent_deployment_engine = AgentDeploymentEngine()
