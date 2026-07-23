import time


class GenesisFollowupEngine:


    def __init__(self):

        self.system = "GENESIS FOLLOW UP ENGINE v1"

        self.followups = []



    def create_sequence(
        self,
        contact
    ):


        sequence = {

            "id":
            "followup_" + str(
                len(self.followups)+1
            ),

            "contact":
            contact,

            "steps":[

                {
                "day":1,
                "action":"Initial Outreach"
                },

                {
                "day":3,
                "action":"Value Follow Up"
                },

                {
                "day":7,
                "action":"Offer Reminder"
                },

                {
                "day":14,
                "action":"Final Check In"
                }

            ],

            "status":
            "ACTIVE",

            "created":
            time.time()

        }


        self.followups.append(sequence)


        return sequence



    def report(self):

        return {

            "system":
            self.system,

            "sequences":
            len(self.followups),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



followup_engine = GenesisFollowupEngine()
