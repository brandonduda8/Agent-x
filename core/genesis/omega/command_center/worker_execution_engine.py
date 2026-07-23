import time
import uuid


from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.result_memory import (
    genesis_result_memory
)


try:
    from core.genesis.omega.command_center.event_bus import (
        genesis_event_bus
    )
except Exception:
    genesis_event_bus = None


class GenesisOmegaWorkerExecutionEngine:

    """
    GENESIS OMEGA WORKER EXECUTION ENGINE v1

    Executes assigned tasks through Omega workers.

    Handles:
    - worker lookup
    - safe execution
    - results
    - events
    - failures
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA WORKER EXECUTION ENGINE v1"
        )

        self.executions = []



    def execute_task(
        self,
        assignment
    ):

        task_id = (
            assignment.get("id")
        )

        capability = (
            assignment.get("capability")
        )

        worker_name = (
            assignment.get("worker")
        )


        worker = (
            genesis_omega_worker_fabric.workers.get(
                capability
            )
        )


        execution = {

            "id":
                "execution_"
                + uuid.uuid4().hex[:8],

            "task":
                assignment.get("task"),

            "worker":
                worker_name,

            "capability":
                capability,

            "status":
                "STARTING",

            "started":
                time.time()

        }


        print(
            "⚙️ Executing:",
            execution["task"],
            "→",
            worker_name
        )


        if not worker:

            execution["status"] = (
                "FAILED_NO_WORKER"
            )

            execution["error"] = (
                "Worker unavailable"
            )

            self.executions.append(
                execution
            )

            return execution



        try:

            result = None


            if hasattr(
                worker,
                "execute"
            ):

                result = (
                    worker.execute(
                        assignment
                    )
                )


            elif hasattr(
                worker,
                "run"
            ):

                result = (
                    worker.run(
                        assignment
                    )
                )


            elif callable(worker):

                result = (
                    worker(
                        assignment
                    )
                )


            else:

                result = {

                    "message":
                        "Worker connected but has no execution interface"

                }



            execution["result"] = result

            execution["status"] = (
                "COMPLETED"
            )



            print(
                "✅ Worker Complete:",
                worker_name
            )



            self.publish_event(
                "WORKER_COMPLETED",
                execution
            )



        except Exception as e:


            execution["status"] = (
                "FAILED"
            )

            execution["error"] = (
                str(e)
            )


            print(
                "❌ Worker Failed:",
                worker_name,
                e
            )


            self.publish_event(
                "WORKER_FAILED",
                execution
            )



        execution["finished"] = (
            time.time()
        )


        self.executions.append(
            execution
        )


        return execution



    def execute_assignments(
        self,
        assignments
    ):

        results = []


        for assignment in assignments:

            results.append(
                self.execute_task(
                    assignment
                )
            )


        memory = genesis_result_memory.store(
            execution_id="batch_" + uuid.uuid4().hex[:8],
            mission="GENESIS OMEGA EXECUTION",
            results=results
        )

        return {

            "system":
                self.system,

            "results":
                results,

            "memory":
                memory,

            "count":
                len(results),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



    def publish_event(
        self,
        event_type,
        data
    ):

        if genesis_event_bus:

            try:

                genesis_event_bus.publish(
                    event_type,
                    data
                )

            except Exception:

                pass



    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(
                    self.executions
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_worker_execution_engine = (
    GenesisOmegaWorkerExecutionEngine()
)
