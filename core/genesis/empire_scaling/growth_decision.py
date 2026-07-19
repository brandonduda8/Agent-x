import uuid
import time


class GrowthDecision:

    def decide(self, evaluation):

        if evaluation["decision"] == "SCALE":

            actions = [
                "Deploy more sales agents",
                "Increase customer acquisition",
                "Expand market presence"
            ]

        else:

            actions = [
                "Optimize operations",
                "Reduce expenses"
            ]


        result = {
            "id": f"growth_{uuid.uuid4().hex[:8]}",
            "decision": evaluation["decision"],
            "actions": actions,
            "timestamp": time.time()
        }


        print("📈 Growth decision generated")

        return result


growth_decision = GrowthDecision()
