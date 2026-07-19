import time

from core.genesis.revenue_intelligence import revenue_intelligence
from core.genesis.memory_engine import memory_engine


class GenesisCEODecisionEngine:


    def __init__(self):

        self.name = "GENESIS CEO DECISION ENGINE v1"

        self.decisions = []



    def evaluate(self, idea):

        analysis = revenue_intelligence.analyze(idea)


        decision = {

            "idea":
                idea,

            "score":
                analysis["overall_score"],

            "action":
                analysis["recommendation"],

            "timestamp":
                time.time()

        }


        self.decisions.append(decision)


        memory_engine.remember_knowledge(

            "business_decision",

            str(decision),

            confidence=0.8

        )


        return decision



    def report(self):

        return {

            "engine":
                self.name,

            "decisions":
                len(self.decisions)

        }



ceo_decision_engine = GenesisCEODecisionEngine()
