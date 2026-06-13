import time

class Supervisor:

    def __init__(self):
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "events": 0
        }

    def log_event(self):
        self.stats["events"] += 1

    def task_done(self):
        self.stats["tasks_completed"] += 1

    def task_failed(self):
        self.stats["tasks_failed"] += 1

    def report(self):

        print("\n[SUPERVISOR REPORT]")
        print("Completed:", self.stats["tasks_completed"])
        print("Failed:", self.stats["tasks_failed"])
        print("Events:", self.stats["events"])
