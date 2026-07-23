import time
import uuid


class GenesisOutreachExecutionAgent:

    """
    GENESIS OUTREACH EXECUTION AGENT v1

    Converts offers into client acquisition actions.
    """

    def __init__(self):

        self.system = (
            "GENESIS OUTREACH EXECUTION AGENT v1"
        )

        self.campaigns = []



    def create_campaign(
        self,
        lead,
        offer
    ):

        campaign = {

            "id":
                "campaign_" + uuid.uuid4().hex[:8],

            "lead":
                lead["id"],

            "company":
                lead["company"],

            "channel":[
                "Email",
                "LinkedIn",
                "Direct Message"
            ],

            "message":
                self.generate_message(
                    lead,
                    offer
                ),

            "follow_up":[

                "Follow up after 3 days",

                "Share automation case study",

                "Schedule discovery call"

            ],

            "status":
                "READY_TO_SEND",

            "created":
                time.time()

        }


        self.campaigns.append(
            campaign
        )


        return campaign



    def generate_message(
        self,
        lead,
        offer
    ):

        return (
            f"Hello {lead['company']},\n\n"
            f"We noticed businesses often struggle with "
            f"{lead['problem']}.\n\n"
            f"We built an {offer['package']} "
            f"that helps companies automate workflows "
            f"and improve customer response.\n\n"
            f"Would you be open to a quick conversation "
            f"about where automation could save time?"
        )



    def report(self):

        return {

            "system":
                self.system,

            "campaigns":
                len(self.campaigns),

            "timestamp":
                time.time()

        }



outreach_execution_agent = GenesisOutreachExecutionAgent()
