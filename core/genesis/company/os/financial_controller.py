import time


class GenesisFinancialController:


    def __init__(self):

        self.system = "GENESIS FINANCIAL CONTROLLER v1"
        self.records = []



    def record(
        self,
        company,
        revenue,
        expenses=0
    ):


        profit = revenue - expenses


        record = {

            "company":
            company,

            "revenue":
            revenue,

            "expenses":
            expenses,

            "profit":
            profit,

            "timestamp":
            time.time()

        }


        self.records.append(record)


        print(
            f"💰 Financial record: ${revenue}"
        )


        return record



    def report(self):

        return {

            "system":
            self.system,

            "records":
            len(self.records),

            "timestamp":
            time.time()

        }



financial_controller = GenesisFinancialController()
