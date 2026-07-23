import time
import threading


from core.genesis.genesis_ceo_autopilot import (
    genesis_ceo_autopilot
)


from core.genesis.telegram_bridge import (
    telegram_bridge
)


class GenesisCEOScheduler:

    """
    GENESIS CEO SCHEDULER v1

    Autonomous executive timer.

    Responsibilities:

    - Run CEO cycles automatically
    - Produce recurring intelligence
    - Notify operator
    - Maintain execution history
    """

    def __init__(self):

        self.system = (
            "GENESIS CEO SCHEDULER v1"
        )

        self.running = False

        self.interval = 86400

        self.cycles = []

        self.thread = None



    def execute_cycle(self):

        print(
            "🧬 CEO SCHEDULER EXECUTING"
        )


        result = (
            genesis_ceo_autopilot
            .run_cycle()
        )


        self.cycles.append(
            result
        )


        message = (
            "👑 GENESIS CEO SCHEDULED REPORT\n\n"
            f"Health: {result.get('health')}\n"
            f"Leads: {result.get('leads')}\n\n"
            "Revenue Targets:\n"
        )


        for target in result.get(
            "revenue_cycle",
            {}
        ).get(
            "targets",
            []
        ):

            message += (
                f"\n• {target.get('title')}"
                f"\n  Score: {target.get('score')}"
                f"\n  Action: {target.get('recommendation')}\n"
            )


        try:

            telegram_bridge.send(
                message
            )

        except Exception:

            pass


        return result



    def loop(self):

        while self.running:

            try:

                self.execute_cycle()

            except Exception as e:

                print(
                    "Scheduler error:",
                    e
                )


            time.sleep(
                self.interval
            )



    def start(
        self,
        interval=None
    ):

        if interval:

            self.interval = interval


        self.running = True


        self.thread = threading.Thread(
            target=self.loop,
            daemon=True
        )


        self.thread.start()


        return {

            "system":
            self.system,

            "status":
            "RUNNING",

            "interval":
            self.interval,

            "timestamp":
            time.time()

        }



    def run_once(self):

        return self.execute_cycle()



    def stop(self):

        self.running = False


        return {

            "system":
            self.system,

            "status":
            "STOPPED",

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "running":
            self.running,

            "cycles":
            len(self.cycles),

            "timestamp":
            time.time()

        }



genesis_ceo_scheduler = GenesisCEOScheduler()



if __name__ == "__main__":

    print(
        genesis_ceo_scheduler.start(
            interval=300
        )
    )

    while True:

        time.sleep(60)
