import time

from core.genesis.executive_controller import (
    executive_controller
)

from core.genesis.autonomous_operation_loop import (
    GenesisAutonomousOperationLoop
)


class GenesisExecutiveBridge:

    """
    GENESIS EXECUTIVE BRIDGE v1

    Connects:
    Executive Controller
    ->
    Autonomous Operations
    ->
    Mission System
    """

    def __init__(self):

        self.name = (
            "GENESIS EXECUTIVE BRIDGE v1"
        )

        self.operation_loop = (
            GenesisAutonomousOperationLoop()
        )

        self.objectives = []

        executive_controller.register(
            self.name,
            self
        )


    def submit_objective(
        self,
        objective
    ):

        event = (
            executive_controller
            .execute_cycle(objective)
        )

        self.objectives.append(
            {
                "objective": objective,
                "timestamp": time.time()
            }
        )

        return event


    def run_cycle(
        self,
        objective=None
    ):

        if objective:

            self.submit_objective(
                objective
            )


        result = (
            self.operation_loop
            .cycle()
        )

        return {
            "bridge":
                self.name,

            "result":
                result,

            "timestamp":
                time.time()
        }


    def status(self):

        return {

            "system":
                self.name,

            "objectives":
                len(self.objectives),

            "cycles":
                self.operation_loop.cycles,

            "timestamp":
                time.time()
        }



executive_bridge = (
    GenesisExecutiveBridge()
)
