import time
import uuid

from core.genesis.client_pipeline import (
    client_pipeline
)

from core.genesis.genesis_lead_intelligence_fabric import (
    genesis_lead_intelligence_fabric
)

from core.genesis.offer_generation_agent import (
    offer_generation_agent
)

from core.genesis.outreach_execution_agent import (
    outreach_execution_agent
)

from core.genesis.event_stream import (
    event_stream
)


class GenesisRevenueAutopilotOrchestrator:

    def __init__(self):

        self.system = (
            "GENESIS REVENUE AUTOPILOT ORCHESTRATOR v2 "
            "WITH LEAD INTELLIGENCE"
        )

        self.cycles = []


    def execute_lead(
        self,
        lead
    ):

        intelligence = (
            genesis_lead_intelligence_fabric
            .enrich_lead(
                lead
            )
        )


        enriched_lead = {
            **lead,
            "intelligence": intelligence
        }


        offer = (
            offer_generation_agent
            .create_offer(
                enriched_lead
            )
        )


        campaign = (
            outreach_execution_agent
            .create_campaign(
                enriched_lead,
                offer
            )
        )


        cycle = {

            "id":
                "revenue_cycle_"
                + uuid.uuid4().hex[:8],

            "lead":
                enriched_lead,

            "intelligence":
                intelligence,

            "offer":
                offer,

            "campaign":
                campaign,

            "status":
                "READY_FOR_EXECUTION",

            "created":
                time.time()
        }


        self.cycles.append(
            cycle
        )


        event_stream.emit(
            "REVENUE_AUTOPILOT_CREATED",
            self.system,
            cycle
        )


        return cycle



    def run_pipeline(
        self
    ):

        results = []


        leads = (
            client_pipeline
            .get_leads()
        )


        for lead in leads:

            results.append(
                self.execute_lead(
                    lead
                )
            )


        return results



    def report(
        self
    ):

        return {

            "system":
                self.system,

            "cycles":
                len(self.cycles),

            "intelligence":
                genesis_lead_intelligence_fabric.report(),

            "timestamp":
                time.time()
        }



revenue_autopilot_orchestrator = (
    GenesisRevenueAutopilotOrchestrator()
)
