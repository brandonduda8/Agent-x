import time
import uuid


class GenesisCompanyBrain:


    def __init__(self):

        self.system = "GENESIS COMPANY BRAIN v1"
        self.decisions = []



    def analyze(
        self,
        company,
        revenue,
        customers
    ):


        print(
            "🧠 Company Brain analyzing"
        )


        if revenue > 0 and customers > 0:

            decision = "SCALE OPERATIONS"

        else:

            decision = "IMPROVE CUSTOMER ACQUISITION"



        result = {

            "id":
            "company_decision_" +
            uuid.uuid4().hex[:8],

            "company":
            company,

            "metrics":
            {
                "revenue": revenue,
                "customers": customers
            },

            "decision":
            decision,

            "timestamp":
            time.time()

        }


        self.decisions.append(result)


        print(
            f"🎯 Company decision: {decision}"
        )


        return result



    def report(self):

        return {

            "system":
            self.system,

            "decisions":
            len(self.decisions),

            "timestamp":
            time.time()

        }



company_brain = GenesisCompanyBrain()
