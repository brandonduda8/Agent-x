import json
import os
import time


class GenesisLeadDatabase:

    def __init__(self):

        self.name = "GENESIS LEAD DATABASE v1"

        self.path = "data/genesis_leads.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.leads = self.load()



    def load(self):

        if os.path.exists(self.path):

            try:
                with open(self.path, "r") as f:
                    return json.load(f)

            except:
                pass

        return []



    def save(self):

        with open(self.path, "w") as f:

            json.dump(
                self.leads,
                f,
                indent=2
            )



    def add_lead(
        self,
        company,
        contact,
        industry
    ):

        lead = {

            "id":
                f"lead_{int(time.time())}",

            "company":
                company,

            "contact":
                contact,

            "industry":
                industry,

            "status":
                "NEW",

            "last_contact":
                None,

            "follow_up":
                None,

            "response":
                None,

            "revenue":
                0,

            "created":
                time.time()

        }


        self.leads.append(
            lead
        )

        self.save()


        return lead



    def update_status(
        self,
        lead_id,
        status
    ):

        for lead in self.leads:

            if lead["id"] == lead_id:

                lead["status"] = status

                lead["last_contact"] = time.time()

                break


        self.save()


        return True



    def get_leads(self):

        return self.leads



    def report(self):

        return {

            "system":
                self.name,

            "leads":
                len(self.leads),

            "timestamp":
                time.time()

        }



lead_database = GenesisLeadDatabase()
