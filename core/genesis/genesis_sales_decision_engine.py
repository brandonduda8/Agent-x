import time
import json
import os
import uuid


class GenesisSalesDecisionEngine:

    def __init__(self):
        self.system = "GENESIS SALES DECISION ENGINE v1"
        self.input_file = "data/genesis_buying_signals.json"
        self.output_file = "data/genesis_sales_decisions.json"
        self.decisions = []

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):

        if os.path.exists(self.output_file):

            try:
                with open(self.output_file, "r") as f:
                    data = json.load(f)

                self.decisions = data.get(
                    "decisions",
                    []
                )

            except Exception:
                self.decisions = []

        else:
            self.save()



    def save(self):

        with open(self.output_file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "decisions": self.decisions,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def load_signals(self):

        if not os.path.exists(self.input_file):
            return []

        try:

            with open(self.input_file, "r") as f:

                data = json.load(f)

            return data.get(
                "signals",
                []
            )

        except Exception:

            return []



    def evaluate_lead(self, lead):

        urgency = lead.get(
            "urgency",
            0
        )

        revenue = lead.get(
            "revenue_impact",
            0
        )

        severity = lead.get(
            "problem_severity",
            0
        )

        score = (
            urgency
            +
            revenue
            +
            severity
        )


        if score >= 200:

            action = "CONTACT_NOW"

        elif score >= 130:

            action = "FOLLOW_UP"

        else:

            action = "NURTURE"


        decision = {

            "id":
                "sales_decision_"
                +
                uuid.uuid4().hex[:8],

            "company":
                lead.get(
                    "company",
                    "Unknown"
                ),

            "lead_id":
                lead.get(
                    "id"
                ),

            "decision":
                action,

            "reason":
                {
                    "urgency": urgency,
                    "revenue_impact": revenue,
                    "problem_severity": severity
                },

            "recommended_offer":
                lead.get(
                    "recommended_offer"
                ),

            "estimated_deal_value":
                lead.get(
                    "estimated_deal_value"
                ),

            "sales_channels":
                [
                    "email",
                    "linkedin",
                    "direct_message"
                ],

            "created":
                time.time()

        }


        return decision



    def run(self):

        signals = self.load_signals()

        results = []


        for lead in signals:

            decision = self.evaluate_lead(
                lead
            )

            results.append(
                decision
            )

            self.decisions.append(
                decision
            )


            print(
                "🎯 Sales Decision:",
                decision["company"],
                "->",
                decision["decision"]
            )


        self.save()


        return {

            "system":
                self.system,

            "processed":
                len(results),

            "decisions":
                results,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()
        }



    def report(self):

        return {

            "system":
                self.system,

            "decisions":
                len(self.decisions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_sales_decision_engine = (
    GenesisSalesDecisionEngine()
)
