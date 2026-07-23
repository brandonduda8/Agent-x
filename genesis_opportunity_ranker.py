import time


class GenesisOpportunityRanker:

    def __init__(self):

        self.weights = {
            "immediate_income": 40,
            "skill_match": 30,
            "career_growth": 20,
            "flexibility": 10
        }


    def rank(self, opportunity, category):

        score = 0
        reasons = []

        if category in ["employment", "jobs"]:
            score += 40
            reasons.append("Immediate income potential")

        if "support" in opportunity.lower():
            score += 30
            reasons.append("Customer service experience match")

        if "technical" in opportunity.lower():
            score += 20
            reasons.append("Computer career transition potential")

        if "ai" in opportunity.lower():
            score += 25
            reasons.append("AI automation growth path")

        return {
            "opportunity": opportunity,
            "score": score,
            "priority": (
                "CRITICAL" if score >= 70
                else "HIGH" if score >= 40
                else "NORMAL"
            ),
            "reasons": reasons,
            "timestamp": time.time()
        }


ranker = GenesisOpportunityRanker()
