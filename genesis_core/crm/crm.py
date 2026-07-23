import time

from genesis_core.memory.database import GenesisDatabase


class GenesisCRM:


    def __init__(self):

        self.database = GenesisDatabase()



    def create_lead(
        self,
        business,
        industry,
        problem,
        value
    ):

        created = time.time()


        self.database.insert(

            "leads",

            [

                None,

                business,

                industry,

                problem,

                "PROSPECTING",

                value,

                created

            ]

        )


        rows = self.database.query(
            "leads"
        )


        lead = rows[-1]


        return {

            "id": lead[0],

            "business": lead[1],

            "industry": lead[2],

            "problem": lead[3],

            "status": lead[4],

            "value": lead[5],

            "created": lead[6]

        }



    def pipeline(self):

        rows = self.database.query(
            "leads"
        )


        return {

            "system":
            "GENESIS CRM FABRIC v2",

            "total_leads":
            len(rows),

            "leads":
            rows,

            "timestamp":
            time.time()

        }
