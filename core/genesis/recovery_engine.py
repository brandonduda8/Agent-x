import time

from core.genesis.self_improvement import self_improvement


class GenesisRecoveryEngine:


    def __init__(self):

        self.name = "GENESIS RECOVERY ENGINE v1"

        self.attempts = []



    def analyze(
        self,
        system,
        error
    ):

        lesson = self_improvement.record_failure(
            system,
            error
        )


        action = lesson["recommendation"]


        recovery = {

            "system":
                system,

            "error":
                error,

            "action":
                action,

            "timestamp":
                time.time(),

            "status":
                "RECOVERY_READY"

        }


        self.attempts.append(
            recovery
        )


        return recovery



    def status(self):

        return {

            "engine":
                self.name,

            "recoveries":
                len(self.attempts),

            "history":
                self.attempts

        }



recovery_engine = GenesisRecoveryEngine()
