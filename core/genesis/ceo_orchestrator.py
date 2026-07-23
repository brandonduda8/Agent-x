import time
import uuid

from core.genesis.brain_router import brain_router
from core.genesis.worker_registry import worker_registry


class GenesisCEOOrchestrator:

    def __init__(self):

        self.system = "GENESIS CEO ORCHESTRATOR v2"

        self.cycles = []



    def analyze_departments(
        self,
        objective
    ):

        objective_lower = objective.lower()

        departments = []


        if any(
            word in objective_lower
            for word in [
                "money",
                "revenue",
                "client",
                "sales",
                "business"
            ]
        ):
            departments.append(
                "Revenue"
            )


        if any(
            word in objective_lower
            for word in [
                "build",
                "code",
                "app",
                "automation",
                "agent",
                "software"
            ]
        ):
            departments.append(
                "Coding"
            )


        if any(
            word in objective_lower
            for word in [
                "research",
                "find",
                "market",
                "opportunity"
            ]
        ):
            departments.append(
                "Research"
            )


        if any(
            word in objective_lower
            for word in [
                "job",
                "career",
                "hire",
                "remote"
            ]
        ):
            departments.append(
                "Career"
            )


        if not departments:

            departments.append(
                "Research"
            )


        return departments



    def run_cycle(
        self,
        objective
    ):

        print(
            "👑 Genesis CEO Mission Started"
        )


        brain = brain_router.route(
            objective
        )


        departments = self.analyze_departments(
            objective
        )


        workers = worker_registry.get_online_workers()


        mission = {

            "id":
                "ceo_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "brain":
                brain,

            "departments":
                departments,

            "available_workers":
                [
                    worker["name"]

                    for worker in workers

                ],

            "tasks":
                [
                    "analyze objective",
                    "select workers",
                    "execute strategy",
                    "measure results",
                    "store learning"
                ],

            "status":
                "READY",

            "created":
                time.time()

        }


        self.cycles.append(
            mission
        )


        print(
            "🧬 Departments:",
            departments
        )


        print(
            "🤖 Workers Available:",
            [
                w["name"]
                for w in workers
            ]
        )


        print(
            "✅ CEO Cycle Created"
        )


        return mission



    def report(
        self
    ):

        return {

            "system":
                self.system,

            "cycles":
                len(
                    self.cycles
                ),

            "timestamp":
                time.time()

        }



ceo_orchestrator = GenesisCEOOrchestrator()
