import time
import uuid

from core.genesis.mission_router import mission_router
from core.genesis.memory_engine import memory_engine


class GenesisCEODecisionLoop:

    """
    GENESIS CEO DECISION LOOP v1

    Responsibilities:

    - Observe Genesis state
    - Evaluate opportunities
    - Choose highest-value objective
    - Create strategic missions
    - Learn from outcomes
    """


    def __init__(self):

        self.system = "GENESIS CEO DECISION LOOP v1"

        self.decisions = []

        self.strategy_memory = []


    def observe(self):

        return {

            "timestamp":
                time.time(),

            "missions":
                len(
                    memory_engine.memory.get(
                        "missions",
                        []
                    )
                ),

            "goal":
                "Increase revenue opportunities"

        }



    def analyze_opportunities(self, state):

        opportunities = [

            {
                "objective":
                "Find AI automation clients needing workflow solutions",

                "priority":
                10
            },


            {
                "objective":
                "Research profitable online business opportunities",

                "priority":
                8
            },


            {
                "objective":
                "Improve Genesis agent capabilities",

                "priority":
                7
            }

        ]


        opportunities.sort(
            key=lambda x:x["priority"],
            reverse=True
        )


        return opportunities[0]



    def create_strategy(self):

        state = self.observe()


        decision = self.analyze_opportunities(
            state
        )


        mission = mission_router.analyze(
            decision["objective"]
        )


        record = {

            "id":
                "decision_" + uuid.uuid4().hex[:8],

            "objective":
                decision["objective"],

            "priority":
                decision["priority"],

            "mission":
                mission,

            "timestamp":
                time.time()

        }


        self.decisions.append(
            record
        )


        self.strategy_memory.append(
            record
        )


        print(
            "🧠 Genesis CEO Decision:"
        )

        print(
            decision["objective"]
        )


        return record



    def status(self):

        return {

            "system":
                self.system,

            "decisions":
                len(
                    self.decisions
                ),

            "timestamp":
                time.time()

        }



ceo_decision_loop = GenesisCEODecisionLoop()
