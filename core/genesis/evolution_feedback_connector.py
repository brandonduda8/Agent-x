import time
import uuid

from core.genesis.agent_evolution_engine import (
    agent_evolution_engine
)


class GenesisEvolutionFeedbackConnector:

    def __init__(self):

        self.system = "GENESIS EVOLUTION FEEDBACK CONNECTOR v1"

        self.evolutions = []

        self.capability_graph = []


    def process_learning(
        self,
        learning
    ):

        performance = learning.get(
            "performance",
            0
        )


        if performance < 0.8:

            return {

                "status":
                    "NO_EVOLUTION_REQUIRED",

                "reason":
                    "Performance below evolution threshold"

            }


        mission = learning.get(
            "mission",
            ""
        )


        agent = "Revenue Agent"


        new_skill = (
            "optimized_"
            + mission.lower()
            .replace(" ", "_")[:40]
        )


        result = agent_evolution_engine.evolve(
            agent,
            new_skill,
            self.capability_graph
        )


        record = {

            "id":
                "evolution_feedback_"
                + uuid.uuid4().hex[:8],

            "learning":
                learning,

            "result":
                result,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }


        self.evolutions.append(
            record
        )


        print(
            "🧬 Learning converted into agent evolution"
        )


        return record



    def report(self):

        return {

            "system":
                self.system,

            "evolutions":
                len(self.evolutions),

            "capabilities":
                len(self.capability_graph),

            "timestamp":
                time.time()

        }



evolution_feedback_connector = GenesisEvolutionFeedbackConnector()
