import time
import json
import os
import uuid


class GenesisDealConversionEngine:

    def __init__(self):

        self.system = (
            "GENESIS DEAL CONVERSION ENGINE v1"
        )

        self.pipeline_file = (
            "data/genesis_client_pipeline.json"
        )

        self.deals_file = (
            "data/genesis_deals.json"
        )

        self.deals = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(
            self.deals_file
        ):

            try:

                with open(
                    self.deals_file,
                    "r"
                ) as f:

                    data = json.load(f)

                    self.deals = data.get(
                        "deals",
                        []
                    )

            except Exception:

                self.deals = []



    def save(self):

        with open(
            self.deals_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system": self.system,
                    "deals": self.deals,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def load_clients(self):

        if not os.path.exists(
            self.pipeline_file
        ):
            return []


        with open(
            self.pipeline_file,
            "r"
        ) as f:

            data = json.load(f)


        return data.get(
            "pipeline",
            []
        )



    def create_deal(
        self,
        client
    ):

        deal = {

            "id":
                "deal_"
                +
                uuid.uuid4().hex[:8],

            "client_id":
                client.get(
                    "id"
                ),

            "company":
                client.get(
                    "company"
                ),

            "offer":
                client.get(
                    "offer"
                ),

            "estimated_value":
                client.get(
                    "estimated_value"
                ),

            "stage":
                "NEW",

            "next_action":
                "SEND_INITIAL_CONTACT",

            "probability":
                10,

            "revenue_status":
                "PENDING",

            "created":
                time.time()

        }


        return deal



    def advance_stage(
        self,
        deal_id,
        stage
    ):

        stages = {

            "NEW": 10,

            "CONTACTED": 20,

            "REPLIED": 40,

            "DISCOVERY_CALL": 60,

            "PROPOSAL_SENT": 70,

            "NEGOTIATION": 80,

            "CLOSED_WON": 100,

            "CLIENT_ONBOARDING": 100

        }


        for deal in self.deals:

            if deal["id"] == deal_id:

                deal["stage"] = stage

                deal["probability"] = (
                    stages.get(
                        stage,
                        10
                    )
                )

                deal["updated"] = time.time()


        self.save()



    def run(self):

        clients = self.load_clients()

        created = []


        existing = [
            d.get("client_id")
            for d in self.deals
        ]


        for client in clients:

            if client.get("id") in existing:

                continue


            deal = self.create_deal(
                client
            )


            self.deals.append(
                deal
            )


            created.append(
                deal
            )


            print(
                "💼 Deal Created:",
                deal["company"]
            )


        self.save()


        return {

            "system":
                self.system,

            "deals_created":
                len(created),

            "deals":
                created,

            "status":
                "READY",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "active_deals":
                len(self.deals),

            "stages":
                [
                    d["stage"]
                    for d in self.deals
                ],

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_deal_conversion_engine = (
    GenesisDealConversionEngine()
)
