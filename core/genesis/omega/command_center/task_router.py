import time
import uuid


from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)


class GenesisOmegaTaskRouter:


    def __init__(self):

        self.system = (
            "GENESIS OMEGA TASK ROUTER v2"
        )

        self.routes = {
            "discover_opportunities":
                "opportunity_discovery",

            "research_targets":
                "opportunity_discovery",

            "generate_solution":
                "revenue",

            "prepare_execution":
                "mission_execution",

            "create_outreach":
                "outreach",

            "qualify_leads":
                "outreach",

            "follow_up_prospects":
                "outreach"
        }

        self.assignments = []



    def ensure_workers(self):

        """
        Self-healing worker connection.
        """

        if (
            not getattr(
                genesis_omega_worker_fabric,
                "workers",
                {}
            )
        ):

            try:

                from core.genesis.omega.genesis_worker_connector import (
                    connect_genesis_workers
                )

                connect_genesis_workers()

                print(
                    "🔄 Task Router Worker Sync Complete"
                )

            except Exception as e:

                print(
                    "Worker sync failed:",
                    e
                )



    def route(
        self,
        execution
    ):


        self.ensure_workers()


        tasks = execution.get(
            "tasks",
            []
        )


        results = []


        for task in tasks:


            capability = (
                self.routes.get(task)
            )


            worker = None


            if capability:

                worker = (
                    genesis_omega_worker_fabric.workers.get(
                        capability
                    )
                )


            assignment = {

                "id":
                    "task_"
                    + uuid.uuid4().hex[:8],

                "task":
                    task,

                "capability":
                    capability,

                "worker":
                    getattr(
                        worker,
                        "name",
                        type(worker).__name__
                        if worker
                        else None
                    ),

                "status":
                    "ASSIGNED"
                    if worker
                    else
                    "NO_WORKER",

                "timestamp":
                    time.time()

            }


            self.assignments.append(
                assignment
            )


            results.append(
                assignment
            )


            print(
                "🔗 Task Routed:",
                task,
                "→",
                assignment["worker"]
            )


        return {

            "system":
                self.system,

            "execution":
                execution["id"],

            "assignments":
                results,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "assignments":
                len(
                    self.assignments
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_task_router = (
    GenesisOmegaTaskRouter()
)
