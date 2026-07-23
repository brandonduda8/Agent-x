import time
import json
import os
import uuid


class GenesisClientAcquisitionEngine:

    def __init__(self):

        self.system = (
            "GENESIS CLIENT ACQUISITION ENGINE v1"
        )

        self.input_file = (
            "data/genesis_outreach_campaigns.json"
        )

        self.pipeline_file = (
            "data/genesis_client_pipeline.json"
        )

        self.followup_file = (
            "data/genesis_followup_queue.json"
        )

        self.pipeline = []
        self.followups = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(self.pipeline_file):

            try:
                with open(self.pipeline_file, "r") as f:
                    self.pipeline = json.load(f).get(
                        "pipeline",
                        []
                    )

            except Exception:
                self.pipeline = []


        if os.path.exists(self.followup_file):

            try:
                with open(self.followup_file, "r") as f:
                    self.followups = json.load(f).get(
                        "followups",
                        []
                    )

            except Exception:
                self.followups = []


    def save(self):

        with open(self.pipeline_file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "pipeline": self.pipeline,
                    "updated": time.time()
                },
                f,
                indent=2
            )


        with open(self.followup_file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "followups": self.followups,
                    "updated": time.time()
                },
                f,
                indent=2
            )


    def load_campaigns(self):

        if not os.path.exists(
            self.input_file
        ):
            return []

        with open(
            self.input_file,
            "r"
        ) as f:

            data = json.load(f)

        return data.get(
            "campaigns",
            []
        )


    def create_pipeline_record(
        self,
        campaign
    ):

        record = {

            "id":
                "client_"
                +
                uuid.uuid4().hex[:8],

            "company":
                campaign.get(
                    "company"
                ),

            "decision":
                campaign.get(
                    "decision"
                ),

            "offer":
                "AI Automation Growth System",

            "estimated_value":
                "$1500 setup + $500/month",

            "status":
                "NEW",

            "outreach_status":
                campaign.get(
                    "status"
                ),

            "channels":
                [
                    "email",
                    "linkedin",
                    "direct_message"
                ],

            "follow_up_schedule":
                [
                    "Day 3 ROI follow-up",
                    "Day 7 case study",
                    "Day 14 final check-in"
                ],

            "created":
                time.time()

        }


        return record



    def create_followup(
        self,
        record
    ):

        return {

            "id":
                "followup_"
                +
                uuid.uuid4().hex[:8],

            "client_id":
                record["id"],

            "company":
                record["company"],

            "next_action":
                "SEND_INITIAL_OUTREACH",

            "status":
                "QUEUED",

            "created":
                time.time()

        }



    def run(self):

        campaigns = self.load_campaigns()

        created = []


        for campaign in campaigns:

            record = self.create_pipeline_record(
                campaign
            )

            self.pipeline.append(
                record
            )


            followup = self.create_followup(
                record
            )

            self.followups.append(
                followup
            )


            created.append(
                record
            )


            print(
                "📊 Client Pipeline Created:",
                record["company"]
            )


        self.save()


        return {

            "system":
                self.system,

            "clients_added":
                len(created),

            "pipeline":
                created,

            "status":
                "READY_FOR_EXECUTION",

            "timestamp":
                time.time()
        }



    def report(self):

        return {

            "system":
                self.system,

            "pipeline_size":
                len(self.pipeline),

            "followups":
                len(self.followups),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_client_acquisition_engine = (
    GenesisClientAcquisitionEngine()
)
