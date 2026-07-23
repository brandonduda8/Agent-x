from genesis_core.memory.learning_memory import GenesisLearningMemory


class GenesisLearningConnector:


    def __init__(self):

        self.memory = GenesisLearningMemory()



    def learn_from_task(
        self,
        task
    ):


        result = task.get(
            "result",
            {}
        )


        memory = self.memory.store(

            "task_completion",

            {

            "mission":
            task.get("mission"),

            "agent":
            task.get("assigned_agent"),

            "result":
            result.get("type"),

            "status":
            result.get("status")

            }

        )


        return memory



    def insights(
        self
    ):

        return self.memory.analyze()
