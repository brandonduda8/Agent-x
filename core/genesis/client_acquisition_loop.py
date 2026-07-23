import time
import uuid


class GenesisClientAcquisitionLoop:

    """
    GENESIS CLIENT ACQUISITION LOOP v1

    Controls:
    - lead qualification
    - scoring
    - pipeline movement
    - duplicate prevention
    """

    def __init__(
        self,
        client_pipeline=None
    ):

        self.system = (
            "GENESIS CLIENT ACQUISITION LOOP v1"
        )

        self.client_pipeline = (
            client_pipeline
        )

        self.activities = []

        self.pipeline_stages = [

            "DISCOVERED",
            "QUALIFIED",
            "CONTACTED",
            "REPLIED",
            "CALL_BOOKED",
            "CLIENT",
            "RECURRING_REVENUE"

        ]



    def score_lead(
        self,
        lead
    ):

        score = 0

        problem = (
            lead.get(
                "problem",
                ""
            )
            .lower()
        )

        opportunity = (
            lead.get(
                "opportunity",
                ""
            )
            .lower()
        )


        if any(
            word in problem
            for word in [
                "manual",
                "slow",
                "repetitive",
                "workflow"
            ]
        ):

            score += 40


        if any(
            word in opportunity
            for word in [
                "automation",
                "ai",
                "communication"
            ]
        ):

            score += 40


        score += 20


        if score >= 80:

            priority = "HIGH"

        elif score >= 50:

            priority = "MEDIUM"

        else:

            priority = "LOW"


        return {

            "lead":
                lead["id"],

            "company":
                lead["company"],

            "score":
                score,

            "priority":
                priority,

            "timestamp":
                time.time()

        }



    def qualify_lead(
        self,
        lead
    ):

        result = self.score_lead(
            lead
        )


        activity = {

            "id":
                "qualification_"
                + uuid.uuid4().hex[:8],

            "lead":
                result,

            "status":
                "QUALIFIED"
                if result["score"] >= 50
                else "REVIEW",

            "created":
                time.time()

        }


        self.activities.append(
            activity
        )


        return activity



    def find_duplicates(
        self
    ):

        seen = {}

        duplicates = []


        if not self.client_pipeline:

            return duplicates


        for lead in (
            self.client_pipeline.get_leads()
        ):

            company = (
                lead["company"]
                .lower()
            )


            if company in seen:

                duplicates.append(
                    lead
                )

            else:

                seen[company] = lead


        return duplicates



    def run_cycle(self):

        results = []


        if not self.client_pipeline:

            return results


        leads = (
            self.client_pipeline
            .get_leads()
        )


        for lead in leads:

            results.append(
                self.qualify_lead(
                    lead
                )
            )


        return results



    def report(self):

        return {

            "system":
                self.system,

            "activities":
                len(self.activities),

            "pipeline_stages":
                self.pipeline_stages,

            "timestamp":
                time.time()

        }



client_acquisition_loop = GenesisClientAcquisitionLoop()
