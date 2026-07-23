from genesis_core.intelligence.opportunity_analyzer import GenesisOpportunityAnalyzer


class GenesisIntelligenceEngine:


    def __init__(self):

        self.analyzer = GenesisOpportunityAnalyzer()


    def analyze_lead(
        self,
        lead
    ):

        return self.analyzer.score(

            lead["problem"],

            lead["value"],

            lead["industry"]

        )
