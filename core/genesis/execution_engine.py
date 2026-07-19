import time
import traceback

from core.genesis.memory_engine import memory_engine
from core.genesis.recovery_engine import recovery_engine
from core.genesis.learning_engine import learning_engine
from core.event_bus import bus


class GenesisExecutionEngine:


    def __init__(self):

        self.name = "GENESIS EXECUTION ENGINE v1.1"

        self.history = []



    async def execute(self, mission):

        print(
            f"⚡ [GENESIS] Executing mission: {mission['objective']}"
        )


        results = []

        failures = []



        for agent in mission["assigned_agents"]:


            try:

                event = {

                    "id":
                        f"genesis_{int(time.time())}",

                    "source":
                        "genesis",

                    "target":
                        agent,

                    "type":
                        "task",

                    "payload":
                    {

                        "objective":
                            mission["objective"]

                    }

                }


                print(
                    f"🧬 Dispatching to {agent}"
                )


                await bus.publish(event)


                results.append(agent)


                learning_engine.analyze_success(

                    agent,

                    mission["objective"],

                    "Task dispatched successfully"

                )



            except Exception as e:


                error = str(e)


                print(
                    f"⚠️ Agent failure: {agent} -> {error}"
                )


                recovery = recovery_engine.analyze(

                    agent,

                    error

                )


                learning_engine.analyze_failure(

                    agent,

                    mission["objective"],

                    error

                )


                failures.append(recovery)



        mission["status"] = (

            "COMPLETED"

            if not failures

            else

            "RECOVERY_REQUIRED"

        )


        mission["executed_agents"] = results


        mission["failures"] = failures


        self.history.append(mission)



        memory_engine.remember_event(

            {

                "type":
                    "mission_complete",

                "mission":
                    mission

            }

        )


        return mission




    def status(self):

        return {

            "engine":
                self.name,

            "missions":
                len(self.history),

            "timestamp":
                time.time()

        }



execution_engine = GenesisExecutionEngine()
