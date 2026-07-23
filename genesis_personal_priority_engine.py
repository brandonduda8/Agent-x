import time


class GenesisPersonalPriorityEngine:

    def __init__(self):
        self.evaluations = []


    def evaluate(self, opportunity):

        title = opportunity.get("title", "").lower()
        category = opportunity.get("category", "").lower()

        score = {
            "income_urgency": 0,
            "experience_match": 0,
            "technology_growth": 0,
            "stability_value": 0,
            "overall": 0
        }

        # Immediate income
        if category in ["employment", "contract"]:
            score["income_urgency"] += 40

        # Existing experience match
        if any(word in title for word in [
            "support",
            "customer",
            "service",
            "technical"
        ]):
            score["experience_match"] += 30

        # Technology pathway
        if any(word in title for word in [
            "technical",
            "software",
            "ai",
            "automation",
            "developer"
        ]):
            score["technology_growth"] += 30

        # Housing priority
        if category == "housing":
            score["stability_value"] += 100

        score["overall"] = sum(score.values())

        if score["overall"] >= 100:
            priority = "CRITICAL"
        elif score["overall"] >= 60:
            priority = "HIGH"
        else:
            priority = "NORMAL"

        result = {
            "opportunity": opportunity.get("title"),
            "category": category,
            "priority_score": score,
            "priority": priority,
            "recommended_action":
                self.route_action(category),
            "timestamp": time.time()
        }

        self.evaluations.append(result)

        return result


    def route_action(self, category):

        routes = {
            "employment":
                "Send to Outreach Agent for application preparation",

            "contract":
                "Send to Revenue Agent for contract pursuit",

            "business_leads":
                "Send to Revenue Agent for client outreach",

            "housing":
                "Send to Stability Agent for contact collection"
        }

        return routes.get(
            category,
            "Send to Zane Hart Agent for review"
        )


    def status(self):

        return {
            "system":
                "GENESIS PERSONAL PRIORITY ENGINE v1",
            "status":
                "ONLINE",
            "evaluations":
                self.evaluations,
            "timestamp":
                time.time()
        }


priority_engine = GenesisPersonalPriorityEngine()
