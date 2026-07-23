import time
import uuid


class GenesisIntelligentWorker:

    def __init__(
        self,
        name,
        capability
    ):

        self.name = name

        self.capability = capability

        self.history = []



    def analyze(
        self,
        objective
    ):

        from core.genesis.brain_router import (
            brain_router
        )


        decision = brain_router.route(
            objective
        )


        return decision



    def execute(
        self,
        objective
    ):

        print(
            "🤖 Intelligent Worker Started:"
        )

        print(
            self.name
        )


        brain = self.analyze(
            objective
        )


        result = {

            "id":
                "worker_"
                +
                uuid.uuid4().hex[:8],

            "worker":
                self.name,

            "capability":
                self.capability,

            "objective":
                objective,

            "brain":
                brain,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }


        self.history.append(
            result
        )


        try:

            from core.genesis.genesis_memory import (
                genesis_memory
            )


            genesis_memory.store_mission(
                result
            )

        except Exception:

            pass


        print(
            "✅ Worker Complete:"
        )

        return result



    def report(
        self
    ):

        return {

            "worker":
                self.name,

            "capability":
                self.capability,

            "executions":
                len(
                    self.history
                ),

            "timestamp":
                time.time()

        }



class WorkerRegistry:

    def __init__(self):

        self.workers = {}



    def register(
        self,
        worker
    ):

        self.workers[
            worker.name
        ] = worker


        print(
            "🧬 Worker Registered:",
            worker.name
        )



    def execute_all(
        self,
        objective
    ):

        results = []


        for worker in self.workers.values():

            results.append(
                worker.execute(
                    objective
                )
            )


        return results



    def report(
        self
    ):

        return {

            "workers":
                list(
                    self.workers.keys()
                ),

            "count":
                len(
                    self.workers
                ),

            "timestamp":
                time.time()

        }



worker_registry = WorkerRegistry()
