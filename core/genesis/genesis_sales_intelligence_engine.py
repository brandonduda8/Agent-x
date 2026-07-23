import time
import uuid


class GenesisSalesIntelligenceEngine:

    def __init__(self):
        self.analyses = []
        self.recommendations = []


    def analyze_prospect(
        self,
        prospect
    ):

        signals = []
        score = 0

        problem = prospect.get(
            "problem",
            ""
        ).lower()

        company = prospect.get(
            "company",
            ""
        ).lower()


        if "manual" in problem:
            score += 30
            signals.append(
                "workflow_pain"
            )

        if "ai" in problem:
            score += 20
            signals.append(
                "ai_interest"
            )

        if "intake" in problem:
            score += 30
            signals.append(
                "high_value_process"
            )

        if company:
            score += 20
            signals.append(
                "business_identified"
            )


        if score >= 80:
            priority = "HOT"
        elif score >= 50:
            priority = "WARM"
        else:
            priority = "COLD"


        analysis = {
            "id":
                f"sales_analysis_{uuid.uuid4().hex[:8]}",
            "prospect":
                prospect.get("id"),
            "company":
                prospect.get("company"),
            "score":
                score,
            "priority":
                priority,
            "signals":
                signals,
            "conversion_probability":
                min(score,100),
            "timestamp":
                time.time()
        }


        self.analyses.append(
            analysis
        )

        return analysis


    def recommend_action(
        self,
        analysis
    ):

        if analysis["priority"] == "HOT":

            action = [
                "Contact immediately",
                "Offer AI demo",
                "Schedule discovery call"
            ]

        elif analysis["priority"] == "WARM":

            action = [
                "Send personalized outreach",
                "Provide case study",
                "Follow up"
            ]

        else:

            action = [
                "Nurture lead",
                "Collect more data"
            ]


        recommendation = {
            "id":
                f"recommendation_{uuid.uuid4().hex[:8]}",
            "prospect":
                analysis["prospect"],
            "priority":
                analysis["priority"],
            "actions":
                action,
            "timestamp":
                time.time()
        }


        self.recommendations.append(
            recommendation
        )

        return recommendation


    def report(self):

        return {
            "system":
                "GENESIS SALES INTELLIGENCE ENGINE v1",
            "analyses":
                len(self.analyses),
            "recommendations":
                len(self.recommendations),
            "status":
                "ONLINE",
            "timestamp":
                time.time()
        }


genesis_sales_intelligence_engine = GenesisSalesIntelligenceEngine()
