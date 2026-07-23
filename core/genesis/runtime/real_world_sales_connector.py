import time
import uuid


class GenesisRealWorldSalesConnector:


    def __init__(
        self,
        database,
        approval,
        queue
    ):

        self.database = database

        self.approval = approval

        self.queue = queue

        self.system = (
            "GENESIS REAL-WORLD SALES CONNECTOR v1"
        )


    def prepare_campaign(
        self,
        business,
        industry,
        problems,
        message
    ):


        lead = self.database.add(

            business,

            industry,

            problems

        )


        approval = self.approval.request(

            "SEND_OUTREACH",

            business

        )


        communication = self.queue.create(

            business,

            message

        )


        return {

            "id":
                "campaign_" +
                uuid.uuid4().hex[:8],

            "system":
                self.system,

            "lead":
                lead,

            "approval":
                approval,

            "communication":
                communication,

            "status":
                "READY_FOR_REVIEW",

            "timestamp":
                time.time()

        }
