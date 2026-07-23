import time
import uuid


class GenesisOpportunityHunter:


    def __init__(
        self,
        revenue_controller=None,
        event_bus=None
    ):

        self.system = (
            "GENESIS AUTONOMOUS OPPORTUNITY HUNTER v1"
        )

        self.revenue_controller = revenue_controller

        self.event_bus = event_bus

        self.discovered = []



    def discover(
        self,
        business,
        industry,
        problem,
        offer,
        estimated_value
    ):


        opportunity = {

            "id":
            "opportunity_" +
            uuid.uuid4().hex[:8],

            "business":
            business,

            "industry":
            industry,

            "problem":
            problem,

            "offer":
            offer,

            "estimated_value":
            estimated_value,

            "score":
            self.score(
                estimated_value
            ),

            "status":
            "DISCOVERED",

            "timestamp":
            time.time()

        }


        self.discovered.append(
            opportunity
        )


        if self.event_bus:

            self.event_bus.publish(
                "OPPORTUNITY_DISCOVERED",
                opportunity
            )


        return opportunity



    def score(
        self,
        value
    ):

        if value >= 5000:
            return "HIGH"

        if value >= 1000:
            return "MEDIUM"

        return "LOW"



    def convert_to_revenue_mission(
        self,
        opportunity
    ):

        if not self.revenue_controller:
            return None


        return self.revenue_controller.create_revenue_mission(
            opportunity["business"],
            opportunity["industry"],
            opportunity["problem"],
            opportunity["offer"],
            opportunity["estimated_value"]
        )



    def report(self):

        return {

            "system":
            self.system,

            "opportunities":
            len(self.discovered),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }


genesis_opportunity_hunter = (
    GenesisOpportunityHunter()
)
