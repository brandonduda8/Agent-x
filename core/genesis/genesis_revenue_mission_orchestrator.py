import time
import uuid

from core.genesis.offer_generation_agent import (
    offer_generation_agent
)

from core.genesis.client_acquisition_engine import (
    client_acquisition_engine
)

from core.genesis.application_agent import (
    application_agent
)


class GenesisRevenueMissionOrchestrator:
    """
    GENESIS REVENUE MISSION ORCHESTRATOR v1

    Converts opportunities into execution plans.

    Routes:

    JOB
      -> Application Agent

    BUSINESS LEAD
      -> Offer Generation
      -> Client Acquisition

    FREELANCE
      -> Application + Offer
    """

    def __init__(self):

        self.system = (
            "GENESIS REVENUE MISSION ORCHESTRATOR v1"
        )

        self.missions = []


    def execute(self, opportunity):

        category = (
            opportunity.get(
                "category",
                ""
            )
            .upper()
        )


        mission = {

            "id":
                "mission_" +
                uuid.uuid4().hex[:8],

            "opportunity":
                opportunity,

            "actions":
                [],

            "status":
                "CREATED",

            "created":
                time.time()

        }


        if category == "JOB":

            package = {

                "title":
                    opportunity.get(
                        "title"
                    ),

                "source":
                    opportunity.get(
                        "source"
                    ),

                "action":
                    "CREATE_APPLICATION_PACKAGE"

            }


            mission["actions"].append(
                package
            )


        elif (
            category == "FREELANCE"
            or category == "CLIENT"
            or category == "BUSINESS"
        ):

            lead = {

                "company":
                    opportunity.get(
                        "title"
                    ),

                "problem":
                    "Business automation opportunity",

                "opportunity":
                    "AI workflow automation"

            }


            offer = (
                offer_generation_agent
                .create_offer(
                    lead
                )
            )


            campaign = (
                client_acquisition_engine
                .create_campaign(
                    opportunity.get(
                        "title"
                    )
                )
            )


            mission["actions"].append(
                offer
            )


            mission["actions"].append(
                campaign
            )


        else:

            mission["actions"].append(
                {
                    "action":
                        "RESEARCH_MORE"
                }
            )


        self.missions.append(
            mission
        )


        print(
            "💰 Revenue Mission Created"
        )


        return mission



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(
                    self.missions
                ),

            "timestamp":
                time.time()

        }



genesis_revenue_mission_orchestrator = (
    GenesisRevenueMissionOrchestrator()
)
