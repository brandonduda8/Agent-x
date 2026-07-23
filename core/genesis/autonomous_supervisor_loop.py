import time
import threading


class AutonomousSupervisorLoop:

    """
    GENESIS AUTONOMOUS SUPERVISOR LOOP v1

    Keeps Genesis operating continuously.
    """


    def __init__(
        self,
        supervisor=None,
        interval=300
    ):

        self.system = "GENESIS AUTONOMOUS SUPERVISOR LOOP v1"

        self.supervisor = supervisor

        self.interval = interval

        self.running = False

        self.thread = None

        self.cycles = 0



    def cycle(self):

        self.cycles += 1


        if self.supervisor:

            return self.supervisor.run_health_check()


        return {
            "status": "NO_SUPERVISOR"
        }



    def start(self):

        if self.running:
            return {
                "status":
                    "ALREADY_RUNNING"
            }


        self.running = True


        def worker():

            while self.running:

                self.cycle()

                time.sleep(
                    self.interval
                )


        self.thread = threading.Thread(
            target=worker,
            daemon=True
        )

        self.thread.start()


        return {

            "system":
                self.system,

            "status":
                "RUNNING",

            "timestamp":
                time.time()
        }



    def stop(self):

        self.running = False


        return {

            "system":
                self.system,

            "status":
                "STOPPED"
        }



    def report(self):

        return {

            "system":
                self.system,

            "running":
                self.running,

            "cycles":
                self.cycles,

            "timestamp":
                time.time()
        }



autonomous_supervisor_loop = AutonomousSupervisorLoop()
