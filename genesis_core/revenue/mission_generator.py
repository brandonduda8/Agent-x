import time
import uuid


class GenesisRevenueMissionGenerator:


    def create(
        self,
        lead
    ):

        return {

            "id":
            "revenue_mission_" +
            uuid.uuid4().hex[:8],

            "objective":
            "Acquire " + lead["business"],

            "offer":
            lead["offer"],

            "tasks":

            [

                "Research decision maker",

                "Create outreach",

                "Follow up lead",

                "Close client"

            ],

            "value":
            lead["value"],

            "status":
            "READY",

            "timestamp":
            time.time()

        }
