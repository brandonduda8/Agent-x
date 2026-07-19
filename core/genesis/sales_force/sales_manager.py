import time
import uuid

from core.genesis.sales_force.prospecting_agent import (
    prospecting_agent
)

from core.genesis.sales_force.research_agent import (
    research_agent
)

from core.genesis.sales_force.outreach_agent import (
    outreach_agent
)

from core.genesis.sales_force.appointment_agent import (
    appointment_agent
)

from core.genesis.sales_force.closer_agent import (
    closer_agent
)


class SalesManager:

    def __init__(self):
        self.cycles = []


    def execute(self, market):

        print("🤖 Sales Manager activated")

        prospects = prospecting_agent.find_prospects(
            market
        )

        research = research_agent.analyze(
            prospects["prospects"]
        )

        campaign = outreach_agent.create_campaign(
            research
        )

        meetings = appointment_agent.schedule(
            campaign
        )

        offers = closer_agent.prepare_offers(
            meetings
        )

        cycle = {
            "id": f"sales_cycle_{uuid.uuid4().hex[:8]}",
            "market": market,
            "prospecting": prospects,
            "research": research,
            "campaign": campaign,
            "meetings": meetings,
            "offers": offers,
            "status": "COMPLETE",
            "timestamp": time.time()
        }

        self.cycles.append(cycle)

        print("🚀 Sales operation complete")

        return cycle


sales_manager = SalesManager()
