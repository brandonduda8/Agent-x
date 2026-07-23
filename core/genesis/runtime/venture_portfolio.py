import time
import uuid


class GenesisVenturePortfolio:


    def __init__(self):

        self.ventures = []


    def add(
        self,
        venture
    ):

        record = {

            "id":
                "venture_" +
                uuid.uuid4().hex[:8],

            "name":
                venture["business"]["business_name"],

            "industry":
                venture["business"]["customer"],

            "status":
                "ACTIVE",

            "revenue":
                0,

            "timestamp":
                time.time()

        }


        self.ventures.append(record)

        return record


    def list(self):

        return self.ventures
