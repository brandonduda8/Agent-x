import time
import uuid

try:
    from core.genesis.omega.learning_loop import (
        genesis_omega_learning_loop
    )
except Exception:
    genesis_omega_learning_loop = None


try:
    from core.genesis.omega.autonomous_workforce_adapter import (
        genesis_omega_workforce_adapter
    )
except Exception:
    genesis_omega_workforce_adapter = None


class GenesisOmegaExecutionAdapter:
    """
    GENESIS OMEGA EXECUTION ADAPTER v3

    Universal execution layer.

    Capability
        |
        v
    Worker Discovery
        |
        +----------------+
        |                |
      Found          Missing
        |                |
        v                v
    Execute       Workforce Repair
                         |
                         v
                   Retry Execute

        |
        v

    Learning Loop
    """

    def __init__(
        self,
        worker_fabric
    ):

        self.system = (
            "GENESIS OMEGA EXECUTION ADAPTER v3"
        )

        self.worker_fabric = worker_fabric
        self.executions = []


    def execute(
        self,
        capability,
        objective
    ):

        worker = self.worker_fabric.get_worker(
            capability
        )


        repair = None


        if not worker:

            print(
                "🧬 Missing Omega Worker:",
                capability
            )


            if genesis_omega_workforce_adapter:

                repair = (
                    genesis_omega_workforce_adapter.repair(
                        capability
                    )
                )


            worker = self.worker_fabric.get_worker(
                capability
            )


        if not worker:

            result = {
                "status": "NO_WORKER",
                "capability": capability,
                "objective": objective,
                "repair": repair
            }

            return result



        execution = {

            "id":
                "omega_execution_"
                + uuid.uuid4().hex[:8],

            "capability":
                capability,

            "worker":
                type(worker).__name__,

            "objective":
                objective,

            "status":
                "STARTED",

            "created":
                time.time()

        }


        try:

            if hasattr(
                worker,
                "execute"
            ):

                result = worker.execute(
                    objective
                )

            elif hasattr(
                worker,
                "run"
            ):

                result = worker.run(
                    objective
                )

            else:

                result = {
                    "message":
                    "Worker has no execution interface"
                }


            execution["result"] = result

            execution["status"] = (
                "COMPLETE"
            )


            if genesis_omega_learning_loop:

                try:

                    genesis_omega_learning_loop.analyze_execution(
                        execution
                    )

                except Exception as e:

                    execution[
                        "learning_error"
                    ] = str(e)



        except Exception as e:

            execution["status"] = (
                "FAILED"
            )

            execution["error"] = str(e)



        self.executions.append(
            execution
        )


        print(
            "⚡ Omega Execution Complete:",
            execution["id"]
        )


        return execution



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
