import time
import uuid

from core.genesis.agent_registry import agent_registry

try:
    from core.genesis.workforce_memory import workforce_memory
except Exception:
    workforce_memory = None

try:
    from core.genesis.persistent_memory_core import (
        genesis_persistent_memory_core
    )
except Exception:
    genesis_persistent_memory_core = None


class GenesisExecutionEngine:

    def __init__(self):

        self.system = (
            "GENESIS EXECUTION ENGINE v1"
        )

        self.executions = []


    def find_agent(
        self,
        required_skill
    ):

        report = agent_registry.report()

        agents = report.get(
            "registry",
            {}
        )

        for name, agent in agents.items():

            skills = agent.get(
                "skills",
                []
            )

            if required_skill in skills:

                return agent

        return None


    def create_task(
        self,
        role,
        objective
    ):

        return {

            "id":
                "task_"
                +
                uuid.uuid4().hex[:8],

            "role":
                role,

            "objective":
                objective,

            "status":
                "ASSIGNED",

            "created":
                time.time()

        }


    def execute_mission(
        self,
        mission
    ):

        execution = {

            "id":
                "execution_"
                +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "tasks": [],

            "status":
                "RUNNING",

            "started":
                time.time()

        }


        workforce = [

            (
                "architecture",
                "Architect"
            ),

            (
                "Python",
                "Software Engineer"
            ),

            (
                "AI",
                "AI Engineer"
            ),

            (
                "testing",
                "QA Scientist"
            ),

            (
                "documentation",
                "Knowledge Engineer"
            )

        ]


        for skill, role in workforce:

            agent = self.find_agent(
                skill
            )

            if agent:

                task = self.create_task(
                    role,
                    mission
                )

                task["agent"] = (
                    agent["name"]
                )

                execution["tasks"].append(
                    task
                )


        execution["status"] = (
            "ASSIGNED"
        )

        execution["completed_assignment"] = (
            len(execution["tasks"])
        )

        self.executions.append(
            execution
        )


        if workforce_memory:

            workforce_memory.add_worker(
                execution
            )


        if genesis_persistent_memory_core:

            genesis_persistent_memory_core.remember(
                "executions",
                execution
            )


        print(
            "⚙️ Genesis Execution Started:",
            execution["id"]
        )


        return execution


    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(self.executions),

            "timestamp":
                time.time()

        }



genesis_execution_engine = (
    GenesisExecutionEngine()
)
