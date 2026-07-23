import time
import uuid


class GenesisOmegaWorkerInterface:
    """
    GENESIS OMEGA UNIVERSAL WORKER INTERFACE v1

    Standard contract for all Omega workers.

    Every worker must support:

    execute()
    report()
    learn()
    """

    def __init__(self, name="UnknownWorker"):
        self.name = name
        self.system = "GENESIS OMEGA UNIVERSAL WORKER INTERFACE v1"
        self.executions = []
        self.learning_events = []


    def execute(self, objective):
        execution = {
            "id": "worker_execution_" + uuid.uuid4().hex[:8],
            "worker": self.name,
            "objective": objective,
            "status": "COMPLETE",
            "result": {
                "message": "Base worker executed"
            },
            "created": time.time()
        }

        self.executions.append(execution)

        return execution


    def learn(self, result):
        event = {
            "id": "worker_learning_" + uuid.uuid4().hex[:8],
            "worker": self.name,
            "execution_id": result.get("id"),
            "insight": "Worker pattern recorded",
            "created": time.time()
        }

        self.learning_events.append(event)

        return event


    def report(self):
        return {
            "system": self.system,
            "worker": self.name,
            "executions": len(self.executions),
            "learning_events": len(self.learning_events),
            "status": "ONLINE",
            "timestamp": time.time()
        }


class GenesisOmegaWorkerAdapter:

    """
    Wraps existing Genesis workers and gives them
    the Omega execution contract.
    """

    def __init__(self, worker, name=None):

        self.worker = worker
        self.name = (
            name
            or
            type(worker).__name__
        )

        self.system = "GENESIS OMEGA WORKER ADAPTER v1"


    def execute(self, objective):

        if hasattr(self.worker, "execute"):

            return self.worker.execute(
                objective
            )


        if hasattr(self.worker, "create_revenue_workflow"):

            mission = {
                "id": "omega_adapter_" + uuid.uuid4().hex[:8],
                "objective": objective,
                "source": "OMEGA_ADAPTER"
            }

            return self.worker.create_revenue_workflow(
                mission
            )


        return {
            "worker": self.name,
            "objective": objective,
            "status": "NO_INTERFACE"
        }


    def learn(self, result):

        return {
            "worker": self.name,
            "execution": result.get("id"),
            "status": "LEARNED",
            "created": time.time()
        }


    def report(self):

        return {
            "system": self.system,
            "worker": self.name,
            "status": "ONLINE",
            "timestamp": time.time()
        }
