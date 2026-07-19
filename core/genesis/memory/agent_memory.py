import time

from core.genesis.memory.memory_store import (
    memory_store
)


class GenesisAgentMemory:

    def __init__(self):

        self.system = "GENESIS AGENT MEMORY v1"


    def remember(
        self,
        agent,
        experience
    ):

        return memory_store.store(
            agent,
            "experience",
            experience
        )


    def learn(
        self,
        agent,
        lesson
    ):

        return memory_store.store(
            agent,
            "lesson",
            lesson
        )


    def recall(
        self,
        agent
    ):

        return memory_store.search(
            agent
        )


    def report(self):

        return {

            "system":
                self.system,

            "timestamp":
                time.time()
        }


agent_memory = GenesisAgentMemory()
