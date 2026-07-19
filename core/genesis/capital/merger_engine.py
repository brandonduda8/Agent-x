import time
import uuid


class MergerEngine:

    def __init__(self):
        self.system = "GENESIS MERGER ENGINE v1"


    def merge(self, company_a, company_b):

        merger = {

            "id":
            "merger_" + uuid.uuid4().hex[:8],

            "companies":
            [
                company_a,
                company_b
            ],

            "new_entity":
            "Genesis " + company_a + " Group",

            "agents_combined":
            True,

            "status":
            "COMPLETE",

            "timestamp":
            time.time()
        }


        print(
            "🤝 Company merger completed"
        )


        return merger



merger_engine = MergerEngine()
