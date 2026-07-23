import time
import uuid


class GenesisRevenueOperator:

    def __init__(self):

        self.system = "GENESIS REVENUE OPERATOR v1.1"
        self.missions = []


    def analyze_opportunity(self, opportunity):

        value = opportunity.get(
            "value",
            0
        )

        if value >= 1000:
            priority = "HIGH"

        elif value >= 500:
            priority = "MEDIUM"

        else:
            priority = "LOW"


        return {
            "priority": priority,
            "value": value,
            "skills": opportunity.get(
                "skills",
                []
            ),
            "timestamp": time.time()
        }


    def normalize_worker(self, worker):

        if isinstance(worker, dict):
            return worker

        return {

            "name":
                getattr(
                    worker,
                    "name",
                    "Unknown Worker"
                ),

            "capability":
                getattr(
                    worker,
                    "capability",
                    ""
                ),

            "skills":
                getattr(
                    worker,
                    "skills",
                    []
                )

        }


    def select_workers(self, workers):

        normalized = [
            self.normalize_worker(worker)
            for worker in workers
        ]


        selected = []


        for worker in normalized:

            capability = str(
                worker.get(
                    "capability",
                    ""
                )
            ).lower()


            if capability in [
                "revenue",
                "research",
                "coding"
            ]:

                selected.append(
                    worker
                )


        if not selected:

            selected = normalized


        return selected



    def create_revenue_plan(self, opportunity):

        title = opportunity.get(
            "title",
            "Opportunity"
        )


        return [

            "Research market demand",

            "Identify ideal customers",

            "Create AI automation offer",

            "Generate proposal",

            "Prepare delivery strategy",

            "Track conversion results"

        ]



    def execute(
        self,
        opportunity,
        workers
    ):

        print(
            "💰 Genesis Revenue Mission Started"
        )


        selected = self.select_workers(
            workers
        )


        mission = {

            "id":
                "revenue_"
                +
                uuid.uuid4().hex[:8],

            "opportunity":
                opportunity.get(
                    "title"
                ),

            "analysis":
                self.analyze_opportunity(
                    opportunity
                ),

            "assigned_workers":
                [
                    worker["name"]
                    for worker in selected
                ],

            "plan":
                self.create_revenue_plan(
                    opportunity
                ),

            "status":
                "READY",

            "created":
                time.time()

        }


        self.missions.append(
            mission
        )


        print(
            "🤖 Assigned:",
            mission["assigned_workers"]
        )

        print(
            "✅ Revenue Mission Ready"
        )


        return mission



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(
                    self.missions
                ),

            "timestamp":
                time.time()

        }



revenue_operator = GenesisRevenueOperator()
