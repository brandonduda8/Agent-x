import time


from core.genesis.omega.genesis_worker_connector import (
    connect_genesis_workers
)


try:

    from core.genesis.omega.learning_loop import (
        genesis_omega_learning_loop
    )

except Exception:

    genesis_omega_learning_loop = None



class GenesisOmegaBootstrap:

    """
    GENESIS OMEGA BOOTSTRAP v2

    Starts:

    - Workers
    - Learning System
    - Capability Fabric
    """



    def __init__(self):

        self.system = (
            "GENESIS OMEGA BOOTSTRAP v2"
        )

        self.started = False

        self.components = []



    def start(self):

        if self.started:

            return {

                "status":
                    "ALREADY_RUNNING"

            }



        workers = connect_genesis_workers()

        self.components.append(
            "WORKER_FABRIC"
        )


        if genesis_omega_learning_loop:

            self.components.append(
                "LEARNING_LOOP"
            )

            print(
                "🧠 Omega Learning Loop Online"
            )



        self.started = True


        print(
            "🚀 Genesis Omega Bootstrap Complete"
        )


        return {

            "system":
                self.system,

            "workers":
                workers,

            "components":
                self.components,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "started":
                self.started,

            "components":
                self.components,

            "timestamp":
                time.time()

        }



genesis_omega_bootstrap = GenesisOmegaBootstrap()
