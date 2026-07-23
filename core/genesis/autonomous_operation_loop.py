import time
import asyncio
import uuid

from core.genesis.mission_queue import mission_queue
from core.genesis.mission_intelligence_router import (
    mission_intelligence_router
)

from core.genesis.execution_engine import (
    execution_engine
)

from core.genesis.mission_outcome_engine import (
    mission_outcome_engine
)

from core.genesis.mission_learning_engine import (
    mission_learning_engine
)

from core.genesis.executive_report_engine import (
    executive_report_engine
)

from core.genesis.event_stream import (
    event_stream
)


class GenesisAutonomousOperationLoop:

    def __init__(self):

        self.name = (
            "GENESIS AUTONOMOUS OPERATION LOOP v7"
        )

        self.cycles = 0
        self.execution_history = []
        self.active_missions = []


    def existing_active_mission(self, objective):

        for mission in mission_queue.queue["missions"]:

            if (
                mission.get("objective") == objective
                and
                mission.get("status") == "ACTIVE"
            ):
                return mission

        return None


    def create_default_mission(self):

        objective = (
            "Find AI automation clients "
            "needing workflow solutions"
        )


        existing = self.existing_active_mission(
            objective
        )


        if existing:

            print(
                "🛡️ Duplicate mission blocked"
            )

            return existing


        decision = (
            mission_intelligence_router
            .analyze(objective)
        )


        mission = {

            "id": decision["id"],

            "objective":
                decision["objective"],

            "assigned_agents":
                decision["assigned_agents"],

            "required_skills":
                decision["required_skills"],

            "priority":
                decision["priority"],

            "status":
                "ACTIVE",

            "created":
                time.time()

        }


        queued = mission_queue.add(

            mission["objective"],

            priority=mission["priority"],

            agents=mission["assigned_agents"],

            skills=mission["required_skills"]

        )


        mission["queue_id"] = (
            queued.get("id")
        )


        self.active_missions.append(
            mission
        )


        event_stream.emit(

            "AUTONOMOUS_MISSION_CREATED",

            self.name,

            mission

        )


        return mission



    def execute_mission(self, mission):

        try:

            result = execution_engine.execute(
                mission
            )


            if hasattr(result, "__await__"):

                result = asyncio.run(result)


            outcome = (
                mission_outcome_engine.evaluate(
                    result,
                    result.get(
                        "results",
                        []
                    )
                )
            )


            result["outcome"] = outcome


            result["executive_report"] = (

                executive_report_engine
                .create_report(
                    mission,
                    outcome
                )

            )


            result["learning"] = (

                mission_learning_engine
                .learn(
                    outcome
                )

            )


            self.execution_history.append(
                result
            )


            event_stream.emit(

                "AUTONOMOUS_MISSION_COMPLETED",

                self.name,

                result

            )


            return result


        except Exception as e:


            failure = {

                "id":
                    "failure_"
                    + uuid.uuid4().hex[:8],

                "status":
                    "FAILED",

                "error":
                    str(e)

            }


            self.execution_history.append(
                failure
            )


            return failure



    def cycle(self):

        self.cycles += 1


        print(
            f"🧬 Autonomous operation cycle #{self.cycles}"
        )


        mission = (
            self.create_default_mission()
        )


        result = (
            self.execute_mission(
                mission
            )
        )


        return result



    def report(self):

        completed = 0
        failed = 0


        for item in self.execution_history:

            if item.get("status") == "FAILED":

                failed += 1

            else:

                completed += 1


        return {

            "system":
                self.name,

            "cycles":
                self.cycles,

            "active_missions":
                len(
                    self.active_missions
                ),

            "executions":
                len(
                    self.execution_history
                ),

            "completed":
                completed,

            "failed":
                failed,

            "timestamp":
                time.time()

        }



genesis_autonomous_operation_loop = (
    GenesisAutonomousOperationLoop()
)
