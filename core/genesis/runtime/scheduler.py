import time


class GenesisScheduler:

    def __init__(self):

        self.system = "GENESIS SCHEDULER v1"
        self.jobs = []


    def add_job(self, name, interval, action):

        self.jobs.append({
            "name": name,
            "interval": interval,
            "action": action,
            "last_run": 0
        })


    def run_once(self):

        now = time.time()

        results = []

        for job in self.jobs:

            if now - job["last_run"] >= job["interval"]:

                result = job["action"]()

                job["last_run"] = now

                results.append({
                    "job": job["name"],
                    "result": result
                })

        return results


scheduler = GenesisScheduler()
