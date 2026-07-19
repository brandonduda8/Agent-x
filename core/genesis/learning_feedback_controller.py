import time
import uuid

from core.genesis.self_improvement_engine import (
    self_improvement_engine
)


class GenesisLearningFeedbackController:

    def __init__(self):

        self.system = "GENESIS LEARNING FEEDBACK CONTROLLER v1"

        self.cycles = []


    def process_execution(
        self,
        execution
    ):

        learning = self_improvement_engine.analyze_execution(
            execution
        )


        cycle = {

            "id":
                "learning_cycle_" + uuid.uuid4().hex[:8],

            "mission":
                execution.get("mission"),

            "learning":
                learning,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }


        self.cycles.append(
            cycle
        )


        print(
            "🔁 Learning feedback processed"
        )


        return cycle



    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                len(self.cycles),

            "timestamp":
                time.time()

        }



learning_feedback_controller = GenesisLearningFeedbackController()
