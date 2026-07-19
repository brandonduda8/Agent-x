import time


from core.genesis.research.opportunity_decision_engine import (
    opportunity_decision_engine
)

from core.genesis.research.opportunity_mission_bridge import (
    opportunity_mission_bridge
)



class GenesisAutonomousBusinessCreator:


    def __init__(self):

        self.system = (
            "GENESIS AUTONOMOUS BUSINESS CREATOR v1"
        )

        self.businesses = []


    def create(self, opportunity):


        decision = (
            opportunity_decision_engine
            .evaluate(opportunity)
        )


        if decision["decision"] != "APPROVED":

            return {

                "status":
                "REJECTED",

                "decision":
                decision

            }


        mission = (
            opportunity_mission_bridge
            .create_mission(
                opportunity
            )
        )


        business = {

            "opportunity":
            opportunity,

            "decision":
            decision,

            "mission":
            mission,

            "status":
            "CREATED",

            "timestamp":
            time.time()

        }


        self.businesses.append(
            business
        )


        print(
            "🏗️ Autonomous business created"
        )


        return business



autonomous_business_creator = (
    GenesisAutonomousBusinessCreator()
)
