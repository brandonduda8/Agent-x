import json
import os
import time


class GenesisBuyingSignalEngine:

    def __init__(self):

        self.system = (
            "GENESIS BUYING SIGNAL INTELLIGENCE v1"
        )

        self.input_file = (
            "data/genesis_priority_queue.json"
        )

        self.output_file = (
            "data/genesis_buying_signals.json"
        )


    def load_queue(self):

        if not os.path.exists(self.input_file):
            return []

        with open(self.input_file, "r") as f:
            data = json.load(f)

        return data.get(
            "priority_queue",
            []
        )


    def analyze(self, lead):

        problem = lead.get(
            "original_problem",
            ""
        ).lower()


        revenue_impact = 50
        urgency = 50
        severity = 50


        if "slow" in problem:
            revenue_impact += 25
            urgency += 20
            severity += 20


        if "manual" in problem:
            severity += 15
            urgency += 10


        industry_multiplier = 20


        estimated_value = (
            "$1500 setup + $500/month"
        )


        score = int(
            (
                lead.get(
                    "automation_score",
                    0
                )
                +
                lead.get(
                    "offer_fit",
                    0
                )
                +
                revenue_impact
                +
                urgency
                +
                severity
                +
                industry_multiplier
            )
            / 6
        )


        action = "NURTURE"


        if score >= 75:
            action = "CONTACT_FIRST"

        elif score >= 55:
            action = "FOLLOW_UP"


        return {

            **lead,

            "revenue_impact":
                revenue_impact,

            "urgency":
                urgency,

            "problem_severity":
                severity,

            "industry_multiplier":
                industry_multiplier,

            "priority_score":
                score,

            "estimated_deal_value":
                estimated_value,

            "recommended_action":
                action,

            "analyzed":
                time.time()
        }



    def build(self):

        leads = self.load_queue()

        results = []


        for lead in leads:

            results.append(
                self.analyze(
                    lead
                )
            )


        results.sort(
            key=lambda x:
            x["priority_score"],
            reverse=True
        )


        with open(
            self.output_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system":
                        self.system,

                    "signals":
                        results,

                    "updated":
                        time.time()
                },
                f,
                indent=2
            )


        return results



    def report(self):

        results = self.build()

        return {

            "system":
                self.system,

            "signals":
                len(results),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_buying_signal_engine = (
    GenesisBuyingSignalEngine()
)
