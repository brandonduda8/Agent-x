import time
import uuid


from core.genesis.autonomy.task_planner import (
    task_planner
)

from core.genesis.autonomy.agent_selector import (
    agent_selector
)


from core.genesis.runtime.agent_runtime import (
    agent_runtime
)



class GenesisWorkerLoop:


    def __init__(self):

        self.system = (
            "GENESIS AUTONOMOUS WORKER LOOP v1"
        )

        self.cycles = []



    def run(
        self,
        objective
    ):

        print(
            "♻️ Genesis worker loop started"
        )


        plan = task_planner.create_plan(
            objective
        )


        executions = []


        for task in plan["tasks"]:


            assignment = agent_selector.select(
                task
            )


            agent = agent_runtime.create_agent(
                assignment["agent"],
                [
                    "analysis",
                    "execution"
                ]
            )


            executions.append({

                "task": task,

                "agent": agent["name"],

                "status": "READY"

            })


        cycle = {

            "id":
            "worker_cycle_" +
            uuid.uuid4().hex[:8],

            "objective": objective,

            "plan": plan,

            "executions": executions,

            "status": "COMPLETE",

            "timestamp": time.time()

        }


        self.cycles.append(cycle)


        print(
            "🚀 Genesis worker loop complete"
        )


        return cycle



    def report(self):

        return {

            "system": self.system,

            "cycles": len(self.cycles),

            "timestamp": time.time()

        }



worker_loop = GenesisWorkerLoop()
