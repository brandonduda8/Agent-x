import time


class GenesisRevenueTracker:


    def __init__(self):

        self.transactions = []


    def record(
        self,
        source,
        amount,
        description
    ):

        transaction = {

            "source":
                source,

            "amount":
                amount,

            "description":
                description,

            "timestamp":
                time.time()

        }


        self.transactions.append(transaction)


        return transaction


    def total(self):

        return sum(

            x["amount"]

            for x in self.transactions

        )
