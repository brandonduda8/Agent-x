import time


class GenesisCompanyDashboard:


    def __init__(self):

        self.system = "GENESIS COMPANY DASHBOARD v1"



    def generate(
        self,
        company,
        revenue,
        customers,
        agents
    ):


        health = "GROWING"


        if revenue == 0:

            health = "NEEDS CUSTOMERS"



        dashboard = {

            "company":
            company,

            "metrics":
            {

                "revenue":
                revenue,

                "customers":
                customers,

                "agents":
                agents

            },

            "health":
            health,

            "timestamp":
            time.time()

        }


        print(
            f"📊 Company health: {health}"
        )


        return dashboard



dashboard = GenesisCompanyDashboard()
