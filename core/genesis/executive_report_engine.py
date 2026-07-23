import time
import uuid
import json
import os


class GenesisExecutiveReportEngine:

    """
    GENESIS EXECUTIVE REPORT ENGINE v1

    Converts:
        Mission Results
              ↓
        Executive Intelligence
              ↓
        Human Report
    """

    def __init__(self):
        self.name = "GENESIS EXECUTIVE REPORT ENGINE v1"
        self.reports = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.path = "data/genesis_reports.json"


    def create_report(
        self,
        mission,
        outcome
    ):

        report = {

            "id":
                "report_" + uuid.uuid4().hex[:8],

            "timestamp":
                time.time(),

            "objective":
                mission.get(
                    "objective",
                    ""
                ),

            "status":
                outcome.get(
                    "status",
                    "UNKNOWN"
                ),

            "success_score":
                outcome.get(
                    "success_score",
                    0
                ),

            "agents":
                outcome.get(
                    "completed_agents",
                    []
                ),

            "capabilities":
                outcome.get(
                    "capabilities_used",
                    []
                ),

            "discoveries":
                outcome.get(
                    "discoveries",
                    []
                ),

            "business_intelligence":
                outcome.get(
                    "business_intelligence",
                    []
                ),

            "next_actions":
                outcome.get(
                    "next_actions",
                    []
                )
        }


        self.reports.append(
            report
        )


        self.save()


        return report



    def save(self):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                self.reports,
                f,
                indent=2
            )



    def latest(self):

        if not self.reports:
            return None

        return self.reports[-1]



    def executive_summary(
        self,
        report
    ):

        return {

            "system":
                self.name,

            "message":
                "Genesis mission report generated",

            "summary":
                {

                "objective":
                    report["objective"],

                "performance":
                    f'{report["success_score"]}/100',

                "agents_completed":
                    len(
                        report["agents"]
                    ),

                "next_priority":
                    report["next_actions"][:3]

                },

            "timestamp":
                time.time()

        }



executive_report_engine = (
    GenesisExecutiveReportEngine()
)
