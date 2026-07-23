import time


class GenesisCommissionEngine:


    def calculate(
        self,
        amount,
        percentage
    ):

        return {

            "revenue":
                amount,

            "commission_percent":
                percentage,

            "commission":
                amount *
                (percentage / 100),

            "timestamp":
                time.time()

        }
