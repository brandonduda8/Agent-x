import uuid
import time


class GrowthForecaster:

    def forecast(self, profit):

        if profit > 3000:
            decision = "SCALE CUSTOMER ACQUISITION"
        else:
            decision = "OPTIMIZE OPERATIONS"

        result = {
            "id": f"forecast_{uuid.uuid4().hex[:8]}",
            "profit": profit,
            "decision": decision,
            "timestamp": time.time()
        }

        print(
            f"📈 Growth decision: {decision}"
        )

        return result


growth_forecaster = GrowthForecaster()
