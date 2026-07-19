import uuid
import time


class ScalingStrategy:

    def create(self, profit):

        if profit > 3000:
            decision = "AGGRESSIVE_SCALE"
        else:
            decision = "OPTIMIZE"

        strategy = {
            "id": f"strategy_{uuid.uuid4().hex[:8]}",
            "profit": profit,
            "decision": decision,
            "priorities": [
                "Acquire customers",
                "Improve automation",
                "Increase revenue"
            ],
            "timestamp": time.time()
        }

        print(
            f"📈 Scaling strategy: {decision}"
        )

        return strategy


scaling_strategy = ScalingStrategy()
