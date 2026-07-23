import time
import uuid
import json
import os


class GenesisClientPipeline:

    """
    GENESIS CLIENT PIPELINE v2

    Persistent revenue pipeline.

    Stores:
    - leads
    - status
    - opportunities
    """

    def __init__(self):

        self.system = (
            "GENESIS CLIENT PIPELINE v2"
        )

        self.file = (
            "workspace/client_pipeline.json"
        )

        self.clients = []

        self.load()



    def load(self):

        os.makedirs(
            "workspace",
            exist_ok=True
        )

        if os.path.exists(self.file):

            try:

                with open(self.file) as f:

                    self.clients = json.load(f)

            except Exception:

                self.clients = []



    def save(self):

        os.makedirs(
            "workspace",
            exist_ok=True
        )

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.clients,
                f,
                indent=2
            )



    def add_lead(
        self,
        company,
        contact,
        problem,
        opportunity
    ):

        lead = {

            "id":
                "lead_" + uuid.uuid4().hex[:8],

            "company":
                company,

            "contact":
                contact,

            "problem":
                problem,

            "opportunity":
                opportunity,

            "status":
                "DISCOVERED",

            "created":
                time.time()

        }


        self.clients.append(
            lead
        )


        self.save()


        return lead



    def get_leads(self):

        return self.clients



    def update_status(
        self,
        lead_id,
        status
    ):

        for lead in self.clients:

            if lead["id"] == lead_id:

                lead["status"] = status

                self.save()

                return lead


        return {
            "status":
                "NOT_FOUND"
        }



    def revenue_report(self):

        stages = {}


        for lead in self.clients:

            status = lead["status"]

            stages[status] = (
                stages.get(status,0)+1
            )


        return {

            "system":
                self.system,

            "total_leads":
                len(self.clients),

            "pipeline":
                stages,

            "timestamp":
                time.time()

        }



client_pipeline = GenesisClientPipeline()
