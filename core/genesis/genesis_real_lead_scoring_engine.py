import os
import json
import time
import uuid


class GenesisRealLeadScoringEngine:

    def __init__(self):

        self.system = "GENESIS REAL LEAD SCORING ENGINE v1"

        self.file = (
            "data/genesis_real_lead_scores.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.scores = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:

                    data = json.load(f)

                self.scores = data.get(
                    "scores",
                    []
                )

            except:

                self.scores = []



    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "scores": self.scores,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def score_lead(self, research):

        pain_score = len(
            research.get(
                "pain_signals",
                []
            )
        ) * 20


        automation_score = research.get(
            "automation_fit_score",
            0
        )


        total = min(
            100,
            pain_score + automation_score
        )


        if total >= 80:

            action = "CONTACT_NOW"

        elif total >= 60:

            action = "FOLLOW_UP"

        else:

            action = "NURTURE"



        result = {

            "id":
                "lead_score_" +
                uuid.uuid4().hex[:8],

            "company":
                research.get(
                    "company"
                ),

            "research_id":
                research.get(
                    "id"
                ),

            "pain_score":
                pain_score,

            "automation_fit":
                automation_score,

            "total_score":
                total,

            "recommended_action":
                action,

            "offer":
                "AI Automation Growth System",

            "estimated_value":
                research.get(
                    "estimated_value"
                ),

            "status":
                "QUALIFIED",

            "created":
                time.time()
        }


        self.scores.append(
            result
        )

        self.save()


        print(
            "🎯 Lead Scored:",
            result["company"],
            "Score:",
            total
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "scored_leads":
                len(self.scores),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_real_lead_scoring_engine = (
    GenesisRealLeadScoringEngine()
)
