import time
import uuid


try:
    from core.genesis.omega.persistent_memory import (
        genesis_omega_persistent_memory
    )
except Exception:
    genesis_omega_persistent_memory = None



class GenesisOmegaLearningLoop:

    """
    GENESIS OMEGA LEARNING LOOP v3

    Converts executions into reusable intelligence.

    Prevents circular memory references.
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA LEARNING LOOP v3"
        )

        self.learning_events = []



    def analyze_execution(
        self,
        execution
    ):

        event = {

            "id":
                "learning_"
                +
                uuid.uuid4().hex[:8],

            "execution_id":
                execution.get(
                    "id"
                ),

            "objective":
                execution.get(
                    "objective"
                ),

            "status":
                execution.get(
                    "status"
                ),

            "capabilities":

                [
                    item.get("capability")
                    for item in execution.get(
                        "executions",
                        []
                    )
                    if isinstance(item, dict)
                ],


            "insight":
                "Execution pattern learned and stored",

            "created":
                time.time()

        }


        self.learning_events.append(
            event
        )


        if genesis_omega_persistent_memory:

            genesis_omega_persistent_memory.remember(
                event
            )


        print(
            "🧠 Omega Learning Event Created:",
            event["id"]
        )


        return event



    def learn(
        self,
        execution
    ):

        return self.analyze_execution(
            execution
        )



    def report(self):

        return {

            "system":
                self.system,

            "learning_events":
                len(
                    self.learning_events
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_omega_learning_loop = (
    GenesisOmegaLearningLoop()
)
