import time
import uuid


class GenesisLeadGenerationEngine:

    def __init__(self):

        self.system = "GENESIS LEAD GENERATION ENGINE v1"

        self.leads = []


    def create_lead(
        self,
        company,
        industry,
        need,
        score,
        source
    ):

        lead = {

            "id":
            "lead_" + uuid.uuid4().hex[:8],

            "company":
            company,

            "industry":
            industry,

            "need":
            need,

            "score":
            score,

            "source":
            source,

            "status":
            "NEW",

            "timestamp":
            time.time()

        }


        self.leads.append(lead)


        print(
            f"🔎 Lead created: {company}"
        )


        return lead



    def qualify_lead(
        self,
        lead_id
    ):

        for lead in self.leads:

            if lead["id"] == lead_id:

                lead["status"] = "QUALIFIED"

                lead["qualified"] = time.time()

                print(
                    f"✅ Lead qualified: {lead['company']}"
                )

                return lead


        return {
            "status":
            "NOT_FOUND"
        }



    def status(self):

        return {

            "system":
            self.system,

            "leads":
            len(self.leads),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



lead_generation_engine = GenesisLeadGenerationEngine()
