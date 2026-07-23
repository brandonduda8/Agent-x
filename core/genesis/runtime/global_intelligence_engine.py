import time


class GenesisGlobalIntelligenceEngine:


    def __init__(
        self,
        scanner,
        scorer
    ):

        self.scanner = scanner
        self.scorer = scorer

        self.system = (
            "GENESIS GLOBAL OPPORTUNITY INTELLIGENCE ENGINE v1"
        )


    def analyze(
        self,
        opportunities
    ):


        scanned = self.scanner.scan(
            opportunities
        )


        scored = []


        for opportunity in scanned["opportunities"]:

            scored.append(

                self.scorer.score(
                    opportunity
                )

            )


        ranked = sorted(

            scored,

            key=lambda x:
            x["revenue_score"],

            reverse=True

        )


        return {

            "system":
                self.system,

            "ranked_opportunities":
                ranked,

            "status":
                "INTELLIGENCE_READY",

            "timestamp":
                time.time()

        }
