import time


class GenesisRevenueDecisionEngine:

    def __init__(self):

        self.system = "GENESIS REVENUE DECISION ENGINE v1"

        self.decisions = []


    def evaluate(self, opportunities):

        print("🧠 Evaluating revenue paths...")


        scored = []


        for item in opportunities:

            name = item["name"]


            if "automation service" in name.lower():

                score = 91

                reason = [
                    "No inventory required",
                    "Can sell immediately",
                    "High ticket potential"
                ]


            elif "consulting" in name.lower():

                score = 86

                reason = [
                    "Fast customer acquisition",
                    "High value service",
                    "Uses existing AI skills"
                ]


            else:

                score = 72

                reason = [
                    "Scalable",
                    "Requires customer acquisition",
                    "Longer timeline"
                ]


            scored.append({

                "opportunity":
                item,

                "score":
                score,

                "reason":
                reason

            })


        scored.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        decision = {

            "winner":
            scored[0],

            "rankings":
            scored,

            "timestamp":
            time.time()

        }


        self.decisions.append(decision)


        return decision



    def report(self):

        return {

            "system":
            self.system,

            "decisions":
            len(self.decisions),

            "timestamp":
            time.time()

        }



revenue_decision_engine = GenesisRevenueDecisionEngine()
