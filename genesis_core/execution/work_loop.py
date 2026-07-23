import time

from genesis_core.execution.execution_manager import GenesisExecutionManager

from genesis_core.execution.result_memory import GenesisResultMemory



class GenesisWorkLoop:


    def __init__(self):

        self.execution = GenesisExecutionManager()

        self.memory = GenesisResultMemory()



    def execute(
        self,
        mission,
        agent,
        objective
    ):

        task = self.execution.create_task(

            mission,

            agent,

            objective

        )


        self.execution.start_task(
            task["id"]
        )


        result = {

            "message":
            "Task execution completed",

            "objective":
            objective

        }


        self.execution.complete_task(

            task["id"],

            result

        )


        self.memory.store(

            task["id"],

            result

        )


        return {

            "system":
            "GENESIS AUTONOMOUS WORK LOOP v1",

            "task":
            task,

            "memory":
            self.memory.all(),

            "timestamp":
            time.time()

        }
