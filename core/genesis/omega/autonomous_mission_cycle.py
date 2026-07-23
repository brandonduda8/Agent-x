import time
import uuid

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.genesis_worker_connector import (
    connect_genesis_workers
)


class GenesisOmegaAutonomousMissionCycle:

    """
    GENESIS OMEGA AUTONOMOUS MISSION CYCLE v2

    Flow:

    Mission
       |
       v
    Worker Bootstrap
       |
       v
    Capability Assignment
       |
       v
    Execution
       |
       v
    Learning
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA AUTONOMOUS MISSION CYCLE v2"
        )

        self.cycles = []

        self.bootstrap()


    def bootstrap(self):

        if len(
            genesis_omega_worker_fabric.list_workers()
        ) == 0:

            connect_genesis_workers()


        print(
            "🚀 Omega Workforce Ready:",
            genesis_omega_worker_fabric.list_workers()
        )


    def run(
        self,
        mission
    ):

        self.bootstrap()

        cycle = {

            "id":
                "omega_cycle_"
                + uuid.uuid4().hex[:8],

            "mission":
                mission,

            "assignments":
                [],

            "results":
                [],

            "status":
                "RUNNING",

            "created":
                time.time()

        }


        for capability in mission.get(
            "capabilities",
            []
        ):

            name = capability.get(
                "capability"
            )

            worker = (
                genesis_omega_worker_fabric
                .get_worker(name)
            )


            cycle["assignments"].append({

                "capability":
                    name,

                "worker_connected":
                    worker is not None,

                "worker":
                    str(type(worker).__name__)
                    if worker else None,

                "status":
                    "ASSIGNED"

            })


        cycle["status"] = "ASSIGNED"

        self.cycles.append(
            cycle
        )


        print(
            "⚡ Omega Mission Cycle Started:",
            cycle["id"]
        )


        return cycle



    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                len(self.cycles),

            "workers":
                genesis_omega_worker_fabric.list_workers(),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_omega_autonomous_mission_cycle = (
    GenesisOmegaAutonomousMissionCycle()
)
