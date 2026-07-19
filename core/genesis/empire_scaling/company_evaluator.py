import uuid
import time


class CompanyEvaluator:

    def evaluate(self, metrics):

        if metrics["profit"] > 3000:
            decision = "SCALE"
        else:
            decision = "OPTIMIZE"

        result = {
            "id": f"evaluation_{uuid.uuid4().hex[:8]}",
            "company": metrics["company"],
            "decision": decision,
            "potential": "HIGH",
            "timestamp": time.time()
        }

        print(
            f"🏢 Company evaluated: {decision}"
        )

        return result


company_evaluator = CompanyEvaluator()
