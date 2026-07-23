import time


class GenesisBusinessIntelligence:


    def __init__(
        self,
        memory,
        tracker,
        analyzer
    ):

        self.memory = memory
        self.tracker = tracker
        self.analyzer = analyzer


        self.system = (
            "GENESIS BUSINESS INTELLIGENCE ENGINE v2"
        )


    def record_result(
        self,
        category,
        entity,
        result
    ):


        self.memory.store(
            category,
            result
        )


        self.tracker.record(
            entity,
            result["status"]
        )


        return {

            "status":
                "RECORDED",

            "timestamp":
                time.time()

        }


    def analyze(
        self
    ):

        return self.analyzer.analyze(

            list(
                self.memory.entries.values()
            )

        )
