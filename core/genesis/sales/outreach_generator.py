import time


class GenesisOutreachGenerator:


    def __init__(self):

        self.system = "GENESIS OUTREACH GENERATOR v1"

        self.messages = []



    def generate(
        self,
        company,
        offer
    ):


        message = {

            "id":
            "outreach_" + str(
                len(self.messages)+1
            ),

            "company":
            company,

            "channel":
            "email",

            "message":
            f"""
Hello,

I noticed {company} may benefit from
{offer}.

Genesis AI systems help businesses automate
repetitive workflows, improve efficiency,
and create new revenue opportunities.

Would you be open to a quick conversation?

Thanks.
""",

            "status":
            "READY",

            "created":
            time.time()

        }


        self.messages.append(message)


        return message



    def report(self):

        return {

            "system":
            self.system,

            "messages":
            len(self.messages),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



outreach_generator = GenesisOutreachGenerator()
