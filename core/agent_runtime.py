import time

from core.capability_registry import capability_registry
from core.agent_heartbeat import heartbeat
from core.intelligence_router import intelligence_router


class AgentRuntime:

    def __init__(self):

        self.name = "GENESIS UNIFIED AGENT RUNTIME"


    def launch(
        self,
        capability,
        task
    ):

        agents = (
            capability_registry
            .find_by_capability(
                capability
            )
        )


        if not agents:

            return {
                "status":
                    "NO_AGENT_FOUND",
                "capability":
                    capability
            }


        agent = agents[0]


        health = heartbeat.report().get(
            agent
        )


        if not health:

            return {
                "status":
                    "AGENT_NOT_REGISTERED"
            }


        model = (
            intelligence_router
            .select_model(
                capability
            )
        )


        result = {

            "runtime":
                self.name,

            "agent":
                agent,

            "capability":
                capability,

            "model":
                model,

            "task":
                task,

            "status":
                "READY_FOR_EXECUTION",

            "timestamp":
                time.time()

        }


        return result



agent_runtime = AgentRuntime()
