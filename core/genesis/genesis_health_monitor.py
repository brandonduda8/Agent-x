import time
import uuid

from core.genesis.event_stream import event_stream


class GenesisHealthMonitor:

    def __init__(
        self,
        runtime_kernel=None,
        telegram_listener=None,
        heartbeat_system=None
    ):

        self.system = "GENESIS HEALTH MONITOR v1"

        self.runtime_kernel = runtime_kernel
        self.telegram_listener = telegram_listener
        self.heartbeat_system = heartbeat_system

        self.checks = []


    def run_check(self):

        report = {

            "id":
            "health_" + uuid.uuid4().hex[:8],

            "system":
            self.system,

            "timestamp":
            time.time(),

            "status":
            "HEALTHY",

            "checks":
            {}

        }


        if self.runtime_kernel:

            report["checks"]["runtime"] = (
                self.runtime_kernel.report()
            )

        else:

            report["checks"]["runtime"] = "NOT_CONNECTED"



        if self.telegram_listener:

            report["checks"]["telegram"] = (
                self.telegram_listener.report()
            )

        else:

            report["checks"]["telegram"] = "NOT_CONNECTED"



        if self.heartbeat_system:

            report["checks"]["heartbeat"] = (
                self.heartbeat_system.report()
            )

        else:

            report["checks"]["heartbeat"] = "NOT_CONNECTED"



        self.checks.append(report)


        event_stream.emit(
            "GENESIS_HEALTH_CHECK",
            self.system,
            report
        )


        return report



    def latest(self):

        if self.checks:

            return self.checks[-1]

        return None



    def report(self):

        return {

            "system":
            self.system,

            "checks":
            len(self.checks),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_health_monitor = GenesisHealthMonitor()
