import time
import uuid


class GenesisDecisionAdapter:

    def __init__(self):

        self.system = "GENESIS DECISION ADAPTER v1"

        self.decisions = []


    def adapt(
        self,
        mission,
        match_result
    ):

        decision = {

            "id":
                "decision_" + uuid.uuid4().hex[:8],

            "objective":
                mission.get(
                    "objective",
                    ""
                ),

            "selected_agents":
                match_result.get(
                    "team",
                    []
                ),

            "scores":
                match_result.get(
                    "scores",
                    {}
                ),

            "status":
                "READY",

            "created":
                time.time()

        }


        self.decisions.append(
            decision
        )


        print(
            "🔗 Genesis decision adapted"
        )


        return decision


    def report(self):

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


genesis_decision_adapter = GenesisDecisionAdapter()
