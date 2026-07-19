import time
import uuid

from core.genesis.memory.agent_memory import (
    agent_memory
)


class GenesisExperienceManager:

    def __init__(self):

        self.system = "GENESIS EXPERIENCE MANAGER v1"
        self.experiences = []


    def record_execution(
        self,
        agent,
        task,
        result
    ):

        experience = {

            "id":
                "experience_" +
                uuid.uuid4().hex[:8],

            "task":
                task,

            "result":
                result,

            "timestamp":
                time.time()
        }


        memory = agent_memory.remember(
            agent,
            experience
        )


        self.experiences.append(
            memory
        )


        print(
            f"📚 Experience recorded: {agent}"
        )


        return memory


    def report(self):

        return {

            "system":
                self.system,

            "experiences":
                len(self.experiences),

            "timestamp":
                time.time()
        }


experience_manager = GenesisExperienceManager()
