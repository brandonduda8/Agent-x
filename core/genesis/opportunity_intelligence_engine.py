import time
import uuid


class GenesisOpportunityIntelligenceEngine:
    """
    GENESIS OPPORTUNITY INTELLIGENCE ENGINE v1

    Finds and ranks income opportunities.

    Converts:
    Jobs
    Freelance gigs
    Client requests

    Into:
    Opportunities
    Scores
    Recommended actions
    """

    def __init__(self):
        self.system = "GENESIS OPPORTUNITY INTELLIGENCE ENGINE v1"
        self.opportunities = []


    def add_opportunity(
        self,
        title,
        source,
        category,
        requirements,
        estimated_value=0
    ):

        opportunity = {

            "id":
                "opp_" + uuid.uuid4().hex[:8],

            "title":
                title,

            "source":
                source,

            "category":
                category,

            "requirements":
                requirements,

            "estimated_value":
                estimated_value,

            "score":
                self.calculate_score(requirements),

            "status":
                "NEW",

            "created":
                time.time()
        }


        self.opportunities.append(opportunity)


        print(
            f"🎯 Opportunity Added: {title}"
        )


        return opportunity



    def calculate_score(self, requirements):

        score = 50


        keywords = [
            "python",
            "automation",
            "api",
            "ai",
            "javascript",
            "data",
            "web"
        ]


        for item in requirements:

            text = item.lower()

            for keyword in keywords:

                if keyword in text:
                    score += 10


        if score > 100:
            score = 100


        return score



    def analyze(self):

        ranked = sorted(
            self.opportunities,
            key=lambda x:x["score"],
            reverse=True
        )


        print(
            "🧠 Opportunity intelligence complete"
        )


        return {

            "system":
                self.system,

            "top_opportunities":
                ranked[:10],

            "timestamp":
                time.time()
        }



    def report(self):

        return {

            "system":
                self.system,

            "opportunities":
                len(self.opportunities),

            "timestamp":
                time.time()
        }



opportunity_intelligence_engine = (
    GenesisOpportunityIntelligenceEngine()
)
