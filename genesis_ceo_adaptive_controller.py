import time

class ZaneHartController:

    def analyze(self, scoreboard):

        decisions = []

        for category, data in scoreboard.items():

            if isinstance(data, dict):

                completed = sum(
                    v for v in data.values()
                    if isinstance(v, int)
                )

                if completed == 0:
                    decisions.append({
                        "category": category,
                        "decision": "CHANGE_STRATEGY",
                        "reason": "No measurable progress"
                    })

                else:
                    decisions.append({
                        "category": category,
                        "decision": "SCALE",
                        "reason": "Positive movement detected"
                    })

        return {
            "system": "GENESIS ZANE HART ADAPTIVE CEO v1",
            "status": "ONLINE",
            "decisions": decisions,
            "timestamp": time.time()
        }


zane_controller = ZaneHartController()
