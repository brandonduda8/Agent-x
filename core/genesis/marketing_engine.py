import time

from core.genesis.memory_engine import memory_engine


class GenesisMarketingEngine:

    def __init__(self):

        self.name = "GENESIS MARKETING ENGINE v1"

        self.campaigns = []



    def analyze_market(self, product):

        product_lower = product.lower()


        if "ai" in product_lower:

            audience = [
                "small business owners",
                "startup founders",
                "online businesses",
                "service companies"
            ]

            problems = [
                "too many customer questions",
                "slow response times",
                "lost sales opportunities",
                "high support costs"
            ]

            angles = [
                "Reduce support costs with AI",
                "Answer customers instantly 24/7",
                "Convert more leads automatically"
            ]


        else:

            audience = [
                "business owners"
            ]

            problems = [
                "saving time",
                "increasing revenue"
            ]

            angles = [
                "Automate repetitive work"
            ]



        campaign = {

            "product":
                product,

            "audience":
                audience,

            "pain_points":
                problems,

            "marketing_angles":
                angles,

            "content": [

                "Educational posts",
                "Customer success stories",
                "Problem/solution videos",
                "Product demonstrations"

            ],

            "outreach": [

                "Cold email campaign",
                "LinkedIn outreach",
                "Direct message campaign"

            ],

            "timestamp":
                time.time()

        }


        self.campaigns.append(
            campaign
        )


        memory_engine.remember_knowledge(
            "marketing_campaign",
            campaign,
            confidence=0.7
        )


        return campaign



    def report(self):

        return {

            "engine":
                self.name,

            "campaigns":
                len(self.campaigns),

            "timestamp":
                time.time()

        }



marketing_engine = GenesisMarketingEngine()
