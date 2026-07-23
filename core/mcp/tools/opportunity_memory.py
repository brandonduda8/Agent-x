import time
import uuid
import json
import os


class OpportunityMemory:

    """
    GENESIS OPPORTUNITY MEMORY MCP v1

    Persistent opportunity intelligence storage.
    """

    def __init__(self):

        self.system = (
            "GENESIS OPPORTUNITY MEMORY MCP v1"
        )

        self.file = (
            "core/mcp/opportunity_memory.json"
        )

        self.opportunities = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.opportunities = json.load(f)

            except Exception:

                self.opportunities = []


    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.opportunities,
                f,
                indent=2
            )


    def store(
        self,
        opportunity
    ):

        record = {

            "id":
            "memory_" +
            uuid.uuid4().hex[:8],

            "opportunity":
            opportunity,

            "status":
            "DISCOVERED",

            "created":
            time.time()

        }


        self.opportunities.append(
            record
        )


        self.save()


        return record



    def search(
        self,
        keyword=None
    ):

        if not keyword:

            return self.opportunities


        results = []


        for item in self.opportunities:

            text = str(
                item
            ).lower()


            if keyword.lower() in text:

                results.append(
                    item
                )


        return results



    def report(self):

        return {

            "system":
            self.system,

            "stored":
            len(
                self.opportunities
            ),

            "timestamp":
            time.time()

        }



opportunity_memory = OpportunityMemory()
