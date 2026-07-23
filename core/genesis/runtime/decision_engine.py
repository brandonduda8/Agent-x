import time


class GenesisDecisionEngine:


    def __init__(
        self,
        memory,
        opportunity,
        resources
    ):

        self.memory = memory
        self.opportunity = opportunity
        self.resources = resources

        self.system = (
            "GENESIS AUTONOMOUS DECISION ENGINE v1"
        )


    def decide(
        self,
        opportunity,
        job,
        workers
    ):


        opportunity_result = (
            self.opportunity.analyze(
                opportunity
            )
        )


        resource_result = (
            self.resources.assign(
                job,
                workers
            )
        )


        decision = {

            "priority":

                opportunity_result,

            "resource_plan":

                resource_result,

            "next_action":

                "CREATE_MISSION"

        }


        self.memory.record(decision)


        return {

            "system":
                self.system,

            "decision":
                decision,

            "status":
                "DECISION_READY",

            "timestamp":
                time.time()

        }
