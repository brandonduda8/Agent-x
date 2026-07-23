import time
import uuid


class GenesisRealityExecutionEngine:


    def __init__(self):

        self.system = (
            "GENESIS REALITY EXECUTION ENGINE v1"
        )

        self.executions = []



    def execute_mission(
        self,
        mission
    ):

        execution_id = (
            "execution_" +
            uuid.uuid4().hex[:8]
        )


        tasks = []


        for action in mission.get(
            "actions",
            []
        ):

            tasks.append({

                "id":
                "task_" +
                uuid.uuid4().hex[:8],

                "action":
                action,

                "status":
                "ASSIGNED",

                "assigned_agent":
                self.select_agent(
                    action,
                    mission.get(
                        "agents",
                        []
                    )
                ),

                "timestamp":
                time.time()

            })


        execution = {

            "id":
            execution_id,

            "mission":
            mission.get(
                "opportunity"
            ),

            "tasks":
            tasks,

            "status":
            "RUNNING",

            "started":
            time.time()

        }


        self.executions.append(
            execution
        )


        return execution



    def select_agent(
        self,
        action,
        agents
    ):

        action = action.lower()


        for agent in agents:

            if (
                "research" in action
                and
                "Research" in agent
            ):
                return agent


            if (
                "outreach" in action
                and
                "Marketing" in agent
            ):
                return agent


            if (
                "demo" in action
                and
                "Coding" in agent
            ):
                return agent


        if agents:

            return agents[0]


        return "Genesis Core"



    def complete_task(
        self,
        execution_id,
        task_id,
        result
    ):

        for execution in self.executions:

            if execution["id"] == execution_id:

                for task in execution["tasks"]:

                    if task["id"] == task_id:

                        task["status"] = "COMPLETE"

                        task["result"] = result

                        task["completed"] = time.time()


                return execution


        return None



    def report(self):

        return {

            "system":
            self.system,

            "executions":
            len(self.executions),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_reality_execution_engine = (
    GenesisRealityExecutionEngine()
)
