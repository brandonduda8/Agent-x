import time
import uuid

from core.genesis.llm_connector import llm_connector


class GenesisAgentWorkerRuntime:

    def __init__(self):
        self.name = "GENESIS AGENT WORKER RUNTIME v1"

        self.execution_history = []

    def get_agent_for_task(self, task):

        role_map = {

            "Genesis Market Research Agent":
                "research",

            "Genesis Product Discovery Agent":
                "reasoning",

            "Genesis Offer Builder Agent":
                "reasoning",

            "Genesis Content Marketing Agent":
                "creative",

            "Genesis Outreach Agent":
                "reasoning",

            "Genesis Analytics Agent":
                "analysis"
        }

        return role_map.get(
            task.get("agent"),
            "reasoning"
        )


    def execute_task(self, task):

        agent = task.get("agent")

        objective = task.get("objective")

        mode = self.get_agent_for_task(task)

        prompt = f"""
You are {agent} inside the Genesis Autonomous Revenue System.

Your mission:

{objective}

Provide an actionable execution report.

Include:

1. Analysis
2. Recommended actions
3. Tools required
4. Automation opportunities
5. Expected outcome
6. Next tasks Genesis should create

"""

        print()
        print("🧠 Genesis Agent Executing:")
        print(agent)

        result = llm_connector.complete(
            mode,
            prompt
        )

        return {

            "task_id": task.get("id"),

            "agent": agent,

            "status":
                result.get(
                    "status",
                    "UNKNOWN"
                ),

            "model":
                result.get(
                    "model"
                ),

            "output":
                result.get(
                    "output"
                ),

            "timestamp":
                time.time()
        }


    def run_execution(self, execution):

        print()
        print(
            "⚙ Genesis Worker Runtime Started"
        )

        execution_id = (
            execution.get("id")
        )

        results = []

        for task in execution.get(
            "tasks",
            []
        ):

            result = self.execute_task(
                task
            )

            results.append(
                result
            )

        report = {

            "id":
                "worker_" +
                uuid.uuid4().hex[:8],

            "execution":
                execution_id,

            "completed_tasks":
                len(results),

            "results":
                results,

            "status":
                "COMPLETED",

            "timestamp":
                time.time()
        }


        self.execution_history.append(
            report
        )

        return report


    def get_status(self):

        return {

            "system":
                self.name,

            "executions_completed":
                len(
                    self.execution_history
                ),

            "timestamp":
                time.time()
        }


agent_worker_runtime = GenesisAgentWorkerRuntime()
