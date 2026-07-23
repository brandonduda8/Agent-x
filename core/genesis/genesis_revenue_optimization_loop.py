import time
import json
import os
import uuid


class GenesisRevenueOptimizationLoop:

    def __init__(self):

        self.system = (
            "GENESIS REVENUE OPTIMIZATION LOOP v1"
        )

        self.responses_file = (
            "data/genesis_client_responses.json"
        )

        self.deals_file = (
            "data/genesis_deals.json"
        )

        self.learning_file = (
            "data/genesis_revenue_learning_memory.json"
        )

        self.learning = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()



    def load(self):

        if os.path.exists(
            self.learning_file
        ):

            try:

                with open(
                    self.learning_file,
                    "r"
                ) as f:

                    data = json.load(f)

                    self.learning = data.get(
                        "learning",
                        []
                    )

            except Exception:

                self.learning = []



    def save(self):

        with open(
            self.learning_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system": self.system,
                    "learning": self.learning,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def load_data(
        self,
        file
    ):

        if not os.path.exists(file):

            return {}


        try:

            with open(
                file,
                "r"
            ) as f:

                return json.load(f)

        except Exception:

            return {}



    def analyze_responses(self):

        data = self.load_data(
            self.responses_file
        )


        responses = data.get(
            "responses",
            []
        )


        insights = {

            "total_responses":
                len(responses),

            "positive_interest":
                0,

            "objections":
                0,

            "unknown":
                0

        }


        for response in responses:

            intent = (
                response
                .get("analysis", {})
                .get("intent")
            )


            if intent == "INTERESTED":

                insights["positive_interest"] += 1


            elif intent == "PRICE_OBJECTION":

                insights["objections"] += 1


            else:

                insights["unknown"] += 1



        return insights



    def analyze_deals(self):

        data = self.load_data(
            self.deals_file
        )


        deals = data.get(
            "deals",
            []
        )


        stages = {}


        for deal in deals:

            stage = deal.get(
                "stage",
                "UNKNOWN"
            )


            stages[stage] = (
                stages.get(stage, 0)
                + 1
            )


        return {

            "total_deals":
                len(deals),

            "stage_distribution":
                stages

        }



    def generate_recommendations(
        self,
        response_data,
        deal_data
    ):


        recommendations = []


        if response_data["objections"] > 0:

            recommendations.append(
                "Improve pricing explanation and ROI messaging"
            )


        if response_data["positive_interest"] > 0:

            recommendations.append(
                "Increase discovery call automation"
            )


        if deal_data["total_deals"] > 0:

            recommendations.append(
                "Continue expanding current target market"
            )


        if not recommendations:

            recommendations.append(
                "Generate more sales data"
            )


        return recommendations



    def run(self):

        response_analysis = (
            self.analyze_responses()
        )


        deal_analysis = (
            self.analyze_deals()
        )


        recommendations = (
            self.generate_recommendations(
                response_analysis,
                deal_analysis
            )
        )


        learning_event = {

            "id":
                "learning_"
                +
                uuid.uuid4().hex[:8],

            "response_analysis":
                response_analysis,

            "deal_analysis":
                deal_analysis,

            "recommendations":
                recommendations,

            "created":
                time.time()

        }


        self.learning.append(
            learning_event
        )


        self.save()


        print(
            "🧠 Revenue Optimization Generated"
        )


        for item in recommendations:

            print(
                "🚀",
                item
            )


        return {

            "system":
                self.system,

            "learning_event":
                learning_event,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "learning_cycles":
                len(self.learning),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_revenue_optimization_loop = (
    GenesisRevenueOptimizationLoop()
)
