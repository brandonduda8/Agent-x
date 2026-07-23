import time

from genesis_core.ceo.decision_engine import GenesisDecisionEngine
from genesis_core.ceo.mission_creator import GenesisMissionCreator



class GenesisCEOLoop:


    def __init__(self):

        self.decision_engine = GenesisDecisionEngine()

        self.mission_creator = GenesisMissionCreator()



    def run_cycle(
        self,
        goal,
        opportunities
    ):


        decision = self.decision_engine.decide(

            opportunities

        )


        mission = None


        if decision["decision"] == "EXECUTE":

            mission = self.mission_creator.create(

                decision

            )


        return {

            "system":
            "GENESIS AUTONOMOUS CEO LOOP v1",

            "goal":
            goal,

            "decision":
            decision,

            "mission":
            mission,

            "timestamp":
            time.time()

        }
