import time
import uuid


class GenesisRealityRevenueNetwork:

    """
    GENESIS REALITY REVENUE NETWORK v1

    Handles verified opportunities.

    Responsibilities:

    - ingest opportunities
    - validate required fields
    - score opportunities
    - route to execution
    """

    def __init__(self):

        self.system = (
            "GENESIS REALITY REVENUE NETWORK v1"
        )

        self.opportunities = []



    def validate_basic(
        self,
        opportunity
    ):

        required = [
            "title",
            "category",
            "source"
        ]

        checks = {}

        for item in required:

            checks[item] = bool(
                opportunity.get(item)
            )


        verified = all(
            checks.values()
        )


        return {

            "verified":
                verified,

            "checks":
                checks

        }



    def score(
        self,
        opportunity
    ):

        score = 0


        if opportunity.get(
            "category"
        ) in [
            "JOB",
            "FREELANCE"
        ]:

            score += 30


        if opportunity.get(
            "url"
        ):

            score += 25


        if opportunity.get(
            "company"
        ):

            score += 25


        if opportunity.get(
            "skills"
        ):

            score += 20


        return score



    def ingest(
        self,
        opportunity
    ):

        validation = (
            self.validate_basic(
                opportunity
            )
        )


        if not validation["verified"]:

            return {

                "status":
                    "REJECTED",

                "reason":
                    "Missing required opportunity data"

            }


        record = {

            "id":
                "revenue_opportunity_"
                +
                uuid.uuid4().hex[:8],

            "opportunity":
                opportunity,

            "validation":
                validation,

            "score":
                self.score(
                    opportunity
                ),

            "status":
                "READY",

            "created":
                time.time()

        }


        self.opportunities.append(
            record
        )


        print(
            "💰 Verified opportunity added:",
            opportunity.get("title")
        )


        return record



    def top_opportunities(
        self
    ):

        return sorted(
            self.opportunities,
            key=lambda x:x["score"],
            reverse=True
        )



    def report(self):

        return {

            "system":
                self.system,

            "opportunities":
                len(
                    self.opportunities
                ),

            "timestamp":
                time.time()

        }



genesis_reality_revenue_network = (
    GenesisRealityRevenueNetwork()
)
