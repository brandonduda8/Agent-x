import time


class GenesisGlobalScannerEngine:


    def __init__(
        self,
        sources,
        scanner,
        ranker
    ):

        self.sources = sources
        self.scanner = scanner
        self.ranker = ranker

        self.system = (
            "GENESIS GLOBAL OPPORTUNITY SCANNER v2"
        )


    def run(self):

        raw = self.sources.collect()


        scanned = self.scanner.scan(

            raw

        )


        ranked = self.ranker.rank(

            scanned["opportunities"]

        )


        return {

            "system":
                self.system,

            "results":
                ranked,

            "status":
                "INTELLIGENCE_READY",

            "timestamp":
                time.time()

        }
