import time

from core.genesis.memory_engine import memory_engine


class GenesisOutreachEngine:

    def __init__(self):

        self.name = "GENESIS OUTREACH ENGINE v1"

        self.campaigns = []



    def create_outreach(self, product, audience):

        campaign = {

            "product":
                product,

            "audience":
                audience,

            "channels": [

                "LinkedIn",
                "Email",
                "Direct Messages"

            ],


            "messages": [

                {
                    "channel":
                        "LinkedIn",

                    "message":
                        f"Hi, I noticed businesses like yours are looking for better ways to improve customer response times. We built {product} to help automate conversations and increase efficiency. Would you be open to seeing how it works?"
                },


                {
                    "channel":
                        "Email",

                    "message":
                        f"Subject: Improving your customer workflow\n\nHi,\n\nMany {audience} spend hours handling repetitive customer requests.\n\n{product} helps automate those conversations and save valuable time.\n\nWould you like a quick demo?"
                },


                {
                    "channel":
                        "DM",

                    "message":
                        f"Hey! Quick question — are you currently using AI to automate customer conversations? We built {product} to help businesses respond faster."
                }

            ],


            "follow_up": [

                "Follow up after 3 days",
                "Share customer benefit",
                "Offer demo",
                "Final check-in"

            ],


            "timestamp":
                time.time()

        }


        self.campaigns.append(
            campaign
        )


        memory_engine.remember_knowledge(
            "outreach_campaign",
            campaign,
            confidence=0.8
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



outreach_engine = GenesisOutreachEngine()
