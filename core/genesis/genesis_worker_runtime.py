import time
import uuid

from core.genesis.llm_connector import llm_connector


class GenesisWorkerRuntime:

    def __init__(self):

        self.name = "GENESIS WORKER RUNTIME v2"

        self.running_tasks = []


    def execute_task(
        self,
        task,
        agent
    ):

        print(
            "🧠 Genesis Agent Executing:"
        )

        print(agent)


        task_record = {

            "id":
                "worker_" +
                uuid.uuid4().hex[:8],

            "task":
                task,

            "agent":
                agent,

            "status":
                "RUNNING",

            "started":
                time.time()

        }


        self.running_tasks.append(
            task_record
        )


        prompt = f"""

You are {agent} inside Genesis Autonomous AI System.

Mission Task:

{task}


Execute your specialized role.

Return:

1. Strategic analysis
2. Recommended actions
3. Revenue impact
4. Next execution steps

Be practical and specific.

"""


        try:

            result = llm_connector.complete(
                "reasoning",
                prompt
            )


            task_record["result"] = result


        except Exception as e:


            task_record["result"] = {

                "status":
                    "LLM_ERROR",

                "error":
                    str(e)

            }



        task_record["status"] = "COMPLETED"

        task_record["completed"] = time.time()


        return task_record



    def run_execution(
        self,
        execution
    ):


        results = []


        for task in execution.get(
            "tasks",
            []
        ):


            result = self.execute_task(

                task.get(
                    "objective"
                ),

                task.get(
                    "agent"
                )

            )


            results.append(
                result
            )


        return {

            "id":

                "worker_run_" +
                uuid.uuid4().hex[:8],


            "execution":

                execution.get(
                    "id"
                ),


            "results":

                results,


            "status":

                "COMPLETED",


            "completed":

                time.time()

        }



    def get_status(self):

        return {

            "system":

                self.name,


            "active_tasks":

                len(
                    self.running_tasks
                ),


            "status":

                "ONLINE",


            "timestamp":

                time.time()

        }



genesis_worker_runtime = GenesisWorkerRuntime()
