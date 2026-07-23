import time


class GenesisAgentPerformanceTracker:


    def __init__(self):

        self.performance = {}

        self.system = (
            "GENESIS AGENT PERFORMANCE TRACKER v1"
        )


    def record(
        self,
        agent,
        success=True
    ):

        if agent not in self.performance:

            self.performance[agent] = {

                "completed": 0,

                "successful": 0

            }


        self.performance[agent]["completed"] += 1


        if success:

            self.performance[agent]["successful"] += 1


        return {

            "agent": agent,

            "performance":
                self.performance[agent],

            "timestamp":
                time.time()

        }


    def get(self):

        return self.performance
