import time


class GenesisRevenueTracker:

    """
    GENESIS REVENUE TRACKER v1

    Tracks economic output.
    """

    def __init__(self):

        self.system = "GENESIS REVENUE TRACKER v1"
        self.transactions = []


    def record(
        self,
        source,
        amount,
        description
    ):

        transaction = {

            "source": source,
            "amount": amount,
            "description": description,
            "timestamp": time.time()

        }

        self.transactions.append(transaction)

        print(
            f"💵 Revenue recorded: ${amount}"
        )

        return transaction


    def total(self):

        return sum(
            x["amount"]
            for x in self.transactions
        )


    def report(self):

        return {

            "system": self.system,

            "transactions":
                len(self.transactions),

            "total":
                self.total(),

            "timestamp":
                time.time()
        }


revenue_tracker = GenesisRevenueTracker()
