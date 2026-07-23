import time
import threading

from core.genesis.genesis_bootstrap import (
    genesis_command_center
)

from core.genesis.telegram_bridge import (
    telegram_bridge
)

from core.genesis.genesis_workforce_controller import (
    genesis_workforce_controller
)

from core.genesis.agent_heartbeat_system import (
    agent_heartbeat_system
)

from core.genesis.event_stream import (
    event_stream
)

from core.genesis.genesis_health_monitor import (
    genesis_health_monitor
)

from core.genesis.genesis_supervisor import (
    GenesisSupervisor
)


class GenesisRuntimeKernel:

    """
    GENESIS RUNTIME KERNEL v2

    Central Genesis operating layer.

    Connected systems:
    - Command Center
    - Workforce
    - Heartbeat
    - Telegram
    - Health Monitor
    - Supervisor
    """

    def __init__(self):

        self.system = (
            "GENESIS RUNTIME KERNEL v2"
        )

        self.running = False

        self.events = []

        self.start_time = time.time()


        self.supervisor = GenesisSupervisor(

            runtime_kernel=self,

            health_monitor=genesis_health_monitor,

            event_stream=event_stream,

            telegram_bridge=telegram_bridge,

            heartbeat_system=agent_heartbeat_system

        )


    def emit(
        self,
        event,
        data=None
    ):

        record = {

            "event": event,

            "data": data,

            "timestamp": time.time()

        }


        self.events.append(record)


        event_stream.emit(

            event,

            self.system,

            record

        )


        try:

            telegram_bridge.send(

                "🧬 GENESIS EVENT\n\n"
                + str(record)

            )

        except Exception:

            pass


        return record



    def status(self):

        return {

            "system": self.system,

            "running": self.running,

            "runtime_seconds":
                int(time.time() - self.start_time),


            "command_center":
                genesis_command_center.generate_report(),


            "workforce":
                genesis_workforce_controller.report(),


            "heartbeat":
                agent_heartbeat_system.workforce_status(),


            "supervisor":
                self.supervisor.report(),


            "events":
                len(self.events),


            "timestamp":
                time.time()

        }



    def heartbeat_loop(self):

        while self.running:


            try:

                health = (
                    self.supervisor.run_health_check()
                )


                telegram_bridge.send(

                    "❤️ GENESIS HEALTH\n\n"
                    + str(health)

                )


            except Exception:

                pass


            time.sleep(300)



    def start(self):

        self.running = True


        self.emit(

            "RUNTIME_KERNEL_STARTED"

        )


        thread = threading.Thread(

            target=self.heartbeat_loop,

            daemon=True

        )


        thread.start()


        return self.status()



    def stop(self):

        self.running = False


        self.emit(

            "RUNTIME_KERNEL_STOPPED"

        )


        return {

            "status":
                "STOPPED",

            "timestamp":
                time.time()

        }



genesis_runtime_kernel = GenesisRuntimeKernel()
