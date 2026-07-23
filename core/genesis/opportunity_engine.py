import time
import uuid

from core.genesis.smart_agent_executor import smart_agent_executor


class OpportunityEngine:


    def __init__(self):

        self.system = "GENESIS OPPORTUNITY ENGINE v1"

        self.opportunities = []



    def analyze(
        self,
        opportunity,
        workers
    ):

        skills = [
            s.lower()
            for s in opportunity.get(
                "skills",
                []
            )
        ]


        score = 0


        if opportunity.get(
            "value",
            0
        ) >= 1000:

            score += 50


        score += (
            len(skills)
            * 10
        )


        result = {

            "id":
                "opp_"
                + uuid.uuid4().hex[:8],

            "title":
                opportunity.get(
                    "title"
                ),

            "value":
                opportunity.get(
                    "value"
                ),

            "score":
                score,

            "workers_available":
                len(
                    workers
                ),

            "status":
                "READY",

            "created":
                time.time()

        }


        self.opportunities.append(
            result
        )


        print(
            "🎯 Opportunity Score:",
            score
        )


        return result



    def execute(
        self,
        opportunity,
        worker
    ):


        analysis = self.analyze(
            opportunity,
            [
                worker
            ]
        )


        execution = smart_agent_executor.execute(
            worker,
            opportunity["title"]
        )


        return {

            "analysis":
                analysis,

            "execution":
                execution

        }



    def report(self):

        return {

            "system":
                self.system,

            "opportunities":
                len(
                    self.opportunities
                )

        }



opportunity_engine = OpportunityEngine()
