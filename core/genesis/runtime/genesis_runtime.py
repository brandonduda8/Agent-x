import time

from core.genesis.runtime.state_manager import state_manager
from core.genesis.runtime.scheduler import scheduler


class GenesisRuntime:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS RUNTIME v1"

        self.running = False

        self.cycles = 0


    def start(self):

        if self.running:

            print(
                "♻️ Genesis Runtime already online"
            )

            return {
                "status": "ALREADY_RUNNING"
            }


        self.running = True


        state_manager.update(
            "runtime",
            "ONLINE"
        )


        state_manager.record_event(
            "RUNTIME_STARTED"
        )


        print(
            "🧬 Genesis Runtime Online"
        )


        return {
            "status":
            "ONLINE"
        }



    def cycle(self):

        if not self.running:

            return {
                "status":
                "OFFLINE"
            }


        self.cycles += 1


        state_manager.update(
            "cycles",
            self.cycles
        )


        state_manager.update(
            "last_cycle",
            time.time()
        )


        state_manager.record_event(
            "CEO_CYCLE_EXECUTED"
        )


        return {

            "cycle":
            self.cycles,

            "status":
            "EXECUTED",

            "timestamp":
            time.time()

        }



    def status(self):

        return {

            "system":
            self.system,

            "running":
            self.running,

            "cycles":
            self.cycles,

            "state":
            state_manager.load()

        }



genesis_runtime = GenesisRuntime()
