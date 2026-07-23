import time


class GenesisVentureStudio:


    def __init__(
        self,
        portfolio,
        scoring,
        allocator
    ):

        self.portfolio = portfolio
        self.scoring = scoring
        self.allocator = allocator

        self.system = (
            "GENESIS AUTONOMOUS VENTURE STUDIO v1"
        )


    def analyze(
        self,
        ventures
    ):


        records = []


        for venture in ventures:

            record = self.portfolio.add(
                venture
            )

            records.append(

                self.scoring.score(
                    record
                )

            )


        decision = self.allocator.allocate(

            records

        )


        return {

            "system":
                self.system,

            "portfolio":
                records,

            "allocation":
                decision,

            "status":
                "STUDIO_OPERATIONAL",

            "timestamp":
                time.time()

        }
