import time
import uuid


class GenesisSalesConversionEngine:
    """
    GENESIS SALES CONVERSION ENGINE v1

    Converts:
        Outreach Responses
              |
              v
        Sales Intelligence

    Handles:
        - CRM pipeline stages
        - lead scoring
        - response classification
        - next actions
        - revenue forecasting
    """

    def __init__(self):
        self.system = "GENESIS SALES CONVERSION ENGINE v1"
        self.pipeline = []


    def add_lead(
        self,
        prospect,
        offer,
        value=2500
    ):

        lead = {

            "id":
                "lead_" + uuid.uuid4().hex[:8],

            "prospect":
                prospect,

            "offer":
                offer,

            "estimated_value":
                value,

            "stage":
                "NEW",

            "score":
                0,

            "probability":
                0,

            "created":
                time.time()
        }


        self.pipeline.append(
            lead
        )


        print(
            f"🎯 Sales lead created: {prospect}"
        )


        return lead



    def analyze_response(
        self,
        lead_id,
        response
    ):

        response_text = response.lower()

        stage = "NO_RESPONSE"
        score = 0
        probability = 0
        next_action = "Follow up later"


        if any(
            word in response_text
            for word in [
                "interested",
                "yes",
                "tell me more",
                "sounds good",
                "schedule"
            ]
        ):

            stage = "INTERESTED"
            score = 90
            probability = 0.80
            next_action = (
                "Schedule discovery call"
            )


        elif any(
            word in response_text
            for word in [
                "maybe",
                "later",
                "send info",
                "think"
            ]
        ):

            stage = "NURTURE"
            score = 50
            probability = 0.40
            next_action = (
                "Start follow-up sequence"
            )


        elif any(
            word in response_text
            for word in [
                "no",
                "not interested"
            ]
        ):

            stage = "CLOSED_LOST"
            score = 10
            probability = 0.05
            next_action = (
                "Store feedback for learning"
            )


        for lead in self.pipeline:

            if lead["id"] == lead_id:

                lead["stage"] = stage
                lead["score"] = score
                lead["probability"] = probability
                lead["next_action"] = next_action
                lead["last_response"] = response
                lead["updated"] = time.time()

                return lead


        return {
            "status":
                "LEAD_NOT_FOUND"
        }



    def forecast_revenue(self):

        total = 0

        for lead in self.pipeline:

            total += (
                lead["estimated_value"]
                *
                lead["probability"]
            )


        return {

            "pipeline_value":
                total,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "leads":
                len(self.pipeline),

            "forecast":
                self.forecast_revenue(),

            "timestamp":
                time.time()

        }



sales_conversion_engine = (
    GenesisSalesConversionEngine()
)
