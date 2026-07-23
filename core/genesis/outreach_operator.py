import time
import uuid


class OutreachOperator:


    def __init__(self):

        self.system = "GENESIS OUTREACH OPERATOR v1"

        self.outreach = []



    def create_lead(
        self,
        business,
        campaign
    ):

        lead = {

            "id":
                "lead_"
                + uuid.uuid4().hex[:8],

            "business":
                business,

            "industry":
                campaign["niche"],

            "offer":
                campaign["offer"],

            "status":
                "NEW",

            "created":
                time.time()

        }


        return lead



    def generate_message(
        self,
        lead
    ):

        return {

            "lead":
                lead["business"],

            "message":
                (
                "Hi, I help "
                + lead["industry"]
                +
                " businesses automate "
                "customer communication and "
                "save time with AI systems. "
                "Would you like a free demo?"
                ),

            "status":
                "READY"

        }



    def launch_campaign(
        self,
        campaign
    ):


        lead = self.create_lead(
            campaign["niche"],
            campaign
        )


        message = self.generate_message(
            lead
        )


        result = {

            "id":
                "outreach_"
                + uuid.uuid4().hex[:8],

            "lead":
                lead,

            "message":
                message,

            "follow_up":
                [
                    "Follow up after 3 days",
                    "Send case study after 7 days",
                    "Final check-in after 14 days"
                ],

            "status":
                "READY",

            "created":
                time.time()

        }


        self.outreach.append(
            result
        )


        print(
            "📨 Genesis Outreach Created"
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "campaigns":
                len(
                    self.outreach
                ),

            "timestamp":
                time.time()

        }



outreach_operator = OutreachOperator()
