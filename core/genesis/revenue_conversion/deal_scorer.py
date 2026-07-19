import uuid
import time


class DealScorer:

    def evaluate(self, company, signals):

        score = 80

        if "automation" in signals:
            score += 10

        if "pain_point" in signals:
            score += 10

        result = {
            "id": f"deal_score_{uuid.uuid4().hex[:8]}",
            "company": company,
            "score": score,
            "probability": round(score / 100, 2),
            "status": "QUALIFIED",
            "timestamp": time.time()
        }

        print("🎯 Deal evaluation complete")

        return result


deal_scorer = DealScorer()
