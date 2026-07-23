import time

from core.genesis.crm.crm_lead_scoring import (
    crm_lead_scoring
)

from core.genesis.crm.crm_pipeline_manager import (
    crm_pipeline_manager
)

from core.genesis.crm.crm_memory_sync import (
    crm_memory_sync
)

from core.genesis.genesis_crm_fabric import (
    genesis_crm_fabric
)



class GenesisRevenueIntelligence:


    def __init__(self):

        self.system = (
            "GENESIS REVENUE INTELLIGENCE v1"
        )

        self.events = []



    def analyze_lead(self, lead):


        score = (
            crm_lead_scoring
            .score(lead)
        )


        crm_memory_sync.remember(
            score
        )


        self.events.append(
            score
        )


        return score



    def create_revenue_opportunity(
        self,
        name,
        email,
        company,
        offer,
        value
    ):


        contact = (
            genesis_crm_fabric
            .create_lead(
                name,
                email,
                company
            )
        )


        deal = (
            genesis_crm_fabric
            .create_opportunity(
                contact,
                offer,
                value
            )
        )


        pipeline = (
            crm_pipeline_manager
            .create_pipeline_item(
                contact,
                offer
            )
        )


        return {

            "contact": contact,

            "deal": deal,

            "pipeline": pipeline,

            "status":
            "CREATED",

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "events":
            len(self.events),

            "pipeline":
            crm_pipeline_manager.report(),

            "memory":
            crm_memory_sync.report(),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_revenue_intelligence = (
    GenesisRevenueIntelligence()
)
