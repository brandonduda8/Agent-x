import time
import uuid


class GenesisMissionOrchestrator:

    """
    GENESIS AUTONOMOUS MISSION ORCHESTRATOR v1

    Converts CEO decisions into executable missions.
    """

    def __init__(
        self,
        kernel=None,
        event_stream=None,
        agent_registry=None
    ):

        self.system = "GENESIS MISSION ORCHESTRATOR v1"

        self.kernel = kernel
        self.event_stream = event_stream
        self.agent_registry = agent_registry

        self.missions = []


    def create_mission(
        self,
        decision
    ):

        mission = {

            "id":
                "mission_" + uuid.uuid4().hex[:8],

            "objective":
                decision["objective"],

            "agents":
                decision["selected_agents"],

            "tasks":
                self.generate_tasks(
                    decision
                ),

            "status":
                "READY",

            "created":
                time.time()
        }


        self.missions.append(mission)


        if self.event_stream:
            self.event_stream.emit(
                "MISSION_CREATED",
                self.system,
                mission
            )


        return mission



    def generate_tasks(
        self,
        decision
    ):

        tasks = []

        for agent in decision["selected_agents"]:

            tasks.append(
                {
                    "id":
                        "task_" + uuid.uuid4().hex[:6],

                    "agent":
                        agent,

                    "status":
                        "READY"
                }
            )

        return tasks



    async def execute(
        self,
        mission
    ):

        mission["status"] = "RUNNING"


        if self.event_stream:
            self.event_stream.emit(
                "MISSION_STARTED",
                self.system,
                mission
            )


        if self.kernel:

            result = await self.kernel.execute(
                mission["objective"]
            )

            mission["result"] = result


        mission["status"] = "COMPLETED"


        if self.event_stream:
            self.event_stream.emit(
                "MISSION_COMPLETED",
                self.system,
                mission
            )


        return mission



    def report(self):

        return {
            "system":
                self.system,

            "missions":
                len(self.missions),

            "timestamp":
                time.time()
        }
