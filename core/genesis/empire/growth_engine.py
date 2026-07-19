import time
import uuid


class GrowthEngine:

    def __init__(self):
        self.system = "GENESIS GROWTH ENGINE v1"


    def evaluate(
        self,
        company
    ):

        if company.get(
            "revenue",
            0
        ) > 0:

            decision = "SCALE"

        else:

            decision = "IMPROVE CUSTOMER ACQUISITION"


        result = {
            "id":
            "growth_" + uuid.uuid4().hex[:8],

            "company":
            company.get("name"),

            "decision":
            decision,

            "timestamp":
            time.time()
        }

        print(
            f"📈 Growth decision: {decision}"
        )

        return result


growth_engine = GrowthEngine()
