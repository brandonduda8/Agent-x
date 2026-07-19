import time
import uuid

from core.genesis.memory.agent_memory import (
    agent_memory
)


class GenesisLearningMemoryConnector:

    def __init__(self):

        self.system = "GENESIS LEARNING MEMORY CONNECTOR v1"
        self.cycles = []


    def store_learning(
        self,
        agent,
        learning
    ):

        record = {

            "id":
                "learning_memory_" +
                uuid.uuid4().hex[:8],

            "agent":
                agent,

            "learning":
                learning,

            "timestamp":
                time.time()
        }


        memory = agent_memory.learn(
            agent,
            record
        )


        self.cycles.append(
            memory
        )


        print(
            "🔁 Learning permanently stored"
        )


        return memory



    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                len(self.cycles),

            "timestamp":
                time.time()
        }



learning_memory_connector = GenesisLearningMemoryConnector()
