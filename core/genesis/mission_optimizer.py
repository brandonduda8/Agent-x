import time
import uuid

from core.genesis.memory.memory_store import (
    memory_store
)


class GenesisMissionOptimizer:

    def __init__(self):

        self.system = "GENESIS MISSION OPTIMIZER v1"
        self.optimizations = []


    def analyze_history(
        self,
        objective
    ):

        memories = memory_store.load()

        matches = []

        for memory in memories.get(
            "memories",
            []
        ):

            content = str(
                memory.get("content")
            ).lower()

            if any(
                word in content
                for word in objective.lower().split()
            ):

                matches.append(
                    memory
                )


        return matches



    def optimize(
        self,
        objective
    ):

        history = self.analyze_history(
            objective
        )


        optimization = {

            "id":
                "optimization_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "historical_matches":
                len(history),

            "recommendation":
                (
                "Use previous successful "
                "strategies and scale execution"
                ),

            "timestamp":
                time.time()
        }


        self.optimizations.append(
            optimization
        )


        print(
            "🧠 Mission strategy optimized"
        )


        return optimization



    def report(self):

        return {

            "system":
                self.system,

            "optimizations":
                len(self.optimizations),

            "timestamp":
                time.time()
        }



mission_optimizer = GenesisMissionOptimizer()
