import time


class GenesisDashboardState:

    """
    GENESIS COMMAND CENTER STATE v1
    """

    def __init__(self):

        self.system = (
            "GENESIS COMMAND CENTER STATE v1"
        )

        self.missions = []
        self.workers = []
        self.activity = []


    def add_activity(
        self,
        event
    ):

        self.activity.append(event)


    def snapshot(self):

        return {
            "system": self.system,
            "missions": self.missions,
            "workers": self.workers,
            "activity": self.activity[-50:],
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_dashboard_state = GenesisDashboardState()
