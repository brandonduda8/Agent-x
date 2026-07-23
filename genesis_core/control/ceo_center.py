import time


class GenesisCEOControlCenter:


    def __init__(
        self,
        database
    ):

        self.database = database



    def status(
        self
    ):

        return {


            "system":
            "GENESIS CEO CONTROL CENTER v1",


            "status":
            "ONLINE",


            "systems":

            [

            "Opportunity Engine",

            "Mission Router",

            "Agent Workforce",

            "Execution Engine",

            "Learning Memory"

            ],


            "memory_count":

            self.database.count(
                "memories"
            ),


            "mission_count":

            self.database.count(
                "missions"
            ),


            "timestamp":
            time.time()

        }



    def daily_brief(
        self,
        opportunities
    ):

        if not opportunities:

            return {

                "message":
                "No opportunities found"

            }


        top = sorted(

            opportunities,

            key=lambda x:
            x["estimated_value"],

            reverse=True

        )[0]


        return {


            "system":
            "GENESIS DAILY CEO BRIEF",


            "top_priority":

            top,


            "recommended_action":

            top["next_action"],


            "timestamp":
            time.time()

        }
