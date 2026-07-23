import time


class GenesisOpportunityRouter:

    def __init__(self):
        self.routes = []


    def route(self, evaluation):

        category = evaluation.get("category")
        priority = evaluation.get("priority")

        if category == "employment":
            agent = "Outreach Agent"
            mission = "Prepare and track job application"

        elif category in ["contract", "business_leads"]:
            agent = "Revenue Agent"
            mission = "Develop revenue opportunity"

        elif category == "housing":
            agent = "Stability Agent"
            mission = "Collect housing resource contacts"

        else:
            agent = "Zane Hart Agent"
            mission = "Review strategic importance"


        route = {
            "id": "route_" + str(len(self.routes)+1),
            "opportunity": evaluation.get("opportunity"),
            "priority": priority,
            "assigned_agent": agent,
            "mission": mission,
            "status": "READY",
            "timestamp": time.time()
        }

        self.routes.append(route)

        return route


    def status(self):

        return {
            "system": "GENESIS OPPORTUNITY ROUTER v1",
            "status": "ONLINE",
            "routes": self.routes,
            "timestamp": time.time()
        }


router = GenesisOpportunityRouter()
