import time
import uuid


class GenesisCRMAgent:

    def __init__(self):

        self.system = "GENESIS CRM AGENT v1"

        self.customers = []

        self.activities = []


    def create_customer(
        self,
        company,
        industry,
        contact,
        need,
        lead_score
    ):

        customer = {

            "id":
            "customer_" + uuid.uuid4().hex[:8],

            "company":
            company,

            "industry":
            industry,

            "contact":
            contact,

            "need":
            need,

            "lead_score":
            lead_score,

            "stage":
            "NEW",

            "assigned_agent":
            "Sales Agent",

            "created":
            time.time()

        }


        self.customers.append(customer)


        print(
            f"🏢 CRM customer created: {company}"
        )


        return customer



    def update_stage(
        self,
        customer_id,
        stage
    ):

        for customer in self.customers:

            if customer["id"] == customer_id:

                customer["stage"] = stage

                customer["updated"] = time.time()


                print(
                    f"📈 Pipeline updated: {stage}"
                )


                return customer


        return {
            "status":
            "NOT_FOUND"
        }



    def add_activity(
        self,
        customer_id,
        activity,
        agent
    ):

        event = {

            "id":
            "activity_" + uuid.uuid4().hex[:8],

            "customer":
            customer_id,

            "activity":
            activity,

            "agent":
            agent,

            "timestamp":
            time.time()

        }


        self.activities.append(event)


        print(
            "📝 CRM activity recorded"
        )


        return event



    def status(self):

        return {

            "system":
            self.system,

            "customers":
            len(self.customers),

            "activities":
            len(self.activities),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



crm_agent = GenesisCRMAgent()
