import time


class GenesisPerformanceRanker:


    def __init__(self):

        self.system = "GENESIS PERFORMANCE RANKER v1"



    def rank(
        self,
        agent
    ):


        score = agent.get(
            "performance",
            0
        )


        if score >= 90:

            level = "ELITE"

        elif score >= 70:

            level = "SENIOR"

        else:

            level = "JUNIOR"


        agent["level"] = level


        print(
            f"📊 {agent['name']} ranked {level}"
        )


        return agent



    def report(self):

        return {

            "system":
            self.system,

            "timestamp":
            time.time()

        }



performance_ranker = GenesisPerformanceRanker()
