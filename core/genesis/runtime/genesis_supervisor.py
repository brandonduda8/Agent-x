import time
import threading

from core.genesis.telegram.telegram_daemon import telegram_daemon
from core.genesis.runtime.genesis_runtime import genesis_runtime
from core.genesis.runtime.scheduler import scheduler
from core.genesis.agent_heartbeat_system import agent_heartbeat_system


class GenesisSupervisor:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS SUPERVISOR v1"

        self.running = False

        self.cycles = 0


    def register_core_agents(self):

        if not agent_heartbeat_system.agents:

            agent_heartbeat_system.register_agent(
                "Genesis Core",
                "Autonomous Intelligence",
                [
                    "orchestration",
                    "decision_making",
                    "automation"
                ]
            )

            agent_heartbeat_system.register_agent(
                "Revenue Engine",
                "Business Growth",
                [
                    "sales",
                    "crm",
                    "lead_generation"
                ]
            )


    def heartbeat_cycle(self):

        while self.running:

            self.cycles += 1

            genesis_runtime.cycle()

            agent_heartbeat_system.heartbeat(
                "Genesis Core",
                "Maintain autonomous system",
                "Supervisor heartbeat"
            )


            try:
                scheduler.run_once()

            except Exception as e:
                print(
                    "Scheduler error:",
                    e
                )


            print(
                f"🧬 Genesis heartbeat #{self.cycles}"
            )

            time.sleep(30)



    def telegram_cycle(self):

        while self.running:

            try:

                telegram_daemon.listen_once()

            except Exception as e:

                print(
                    "Telegram error:",
                    e
                )


            time.sleep(3)



    def start(self):

        print("=" * 60)
        print("🧬 GENESIS AUTONOMOUS SUPERVISOR ONLINE")
        print("=" * 60)


        self.register_core_agents()


        genesis_runtime.start()

        telegram_daemon.start()


        self.running = True


        threading.Thread(
            target=self.heartbeat_cycle,
            daemon=True
        ).start()


        threading.Thread(
            target=self.telegram_cycle,
            daemon=True
        ).start()


        print(
            "✅ Genesis Supervisor running"
        )


        return self.status()



    def status(self):

        return {

            "system":
                self.system,

            "running":
                self.running,

            "cycles":
                self.cycles,

            "runtime":
                genesis_runtime.status(),

            "agents":
                agent_heartbeat_system.workforce_status()

        }



genesis_supervisor = GenesisSupervisor()



if __name__ == "__main__":

    genesis_supervisor.start()


    while True:

        time.sleep(60)
