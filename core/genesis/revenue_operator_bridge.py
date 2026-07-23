import time

from core.genesis.genesis_revenue_operator import (
    genesis_revenue_operator
)


class GenesisRevenueOperatorBridge:

    """
    GENESIS REVENUE OPERATOR BRIDGE v1

    Connects Genesis missions
    into revenue execution.
    """

    def __init__(self):

        self.system = (
            "GENESIS REVENUE OPERATOR BRIDGE v1"
        )

        self.history = []


    def activate(
        self,
        missions
    ):

        result = (
            genesis_revenue_operator
            .execute_pipeline(
                missions
            )
        )


        record = {

            "system":
                self.system,

            "missions":
                len(missions),

            "result":
                result,

            "status":
                "ACTIVATED",

            "timestamp":
                time.time()

        }


        self.history.append(
            record
        )


        return record


    def report(self):

        return {

            "system":
                self.system,

            "activations":
                len(
                    self.history
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }


genesis_revenue_operator_bridge = GenesisRevenueOperatorBridge()
