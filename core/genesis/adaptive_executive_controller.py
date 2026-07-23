import time
import uuid

from core.genesis.mission_optimizer import (
    mission_optimizer
)

from core.genesis.executive_mission_orchestrator import (
    executive_mission_orchestrator
)

from core.genesis.memory.business_cycle_memory_bridge import (
    business_cycle_memory_bridge
)

from core.genesis.genesis_adaptive_ceo_learning_bridge import (
    genesis_adaptive_ceo_learning_bridge
)


class GenesisAdaptiveExecutiveController:

    def __init__(self):

        self.system = (
            "GENESIS ADAPTIVE EXECUTIVE CONTROLLER v2 "
            "WITH CEO LEARNING"
        )

        self.cycles = []


    def evaluate_objective(
        self,
        objective
    ):

        print(
            f"👑 Executive objective received: {objective}"
        )


        intelligence = (
            mission_optimizer.optimize(
                objective
            )
        )


        learning = (
            genesis_adaptive_ceo_learning_bridge
            .advise_future_mission(
                objective
            )
        )


        print(
            "🧠 CEO learning applied"
        )


        mission = (
            executive_mission_orchestrator
            .create_mission(
                objective
            )
        )


        return {

            "intelligence":
                intelligence,

            "ceo_learning":
                learning,

            "mission":
                mission

        }



    def complete_cycle(
        self,
        objective,
        result
    ):

        cycle = {

            "id":
                "adaptive_cycle_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "result":
                result,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }


        business_cycle_memory_bridge.record_cycle(
            cycle
        )


        self.cycles.append(
            cycle
        )


        print(
            "🧠 Adaptive executive cycle stored"
        )


        return cycle



    def run(
        self,
        objective
    ):

        intelligence = (
            self.evaluate_objective(
                objective
            )
        )


        cycle = (
            self.complete_cycle(
                objective,
                intelligence
            )
        )


        return cycle



    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                len(
                    self.cycles
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



adaptive_executive_controller = (
    GenesisAdaptiveExecutiveController()
)
