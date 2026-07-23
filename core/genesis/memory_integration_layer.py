import time


class GenesisMemoryIntegrationLayer:

    """
    GENESIS MEMORY INTEGRATION LAYER v1

    Connects Genesis systems to
    persistent memory.

    Responsibilities:

    - record worker activity
    - record opportunities
    - record executions
    - record improvements
    - create intelligence reports
    """

    def __init__(self):

        self.system = (
            "GENESIS MEMORY INTEGRATION LAYER v1"
        )


    def remember(
        self,
        category,
        data
    ):

        from core.genesis.persistent_memory_core import (
            genesis_persistent_memory_core
        )

        return (
            genesis_persistent_memory_core
            .remember(
                category,
                data
            )
        )



    def remember_opportunity(
        self,
        opportunity
    ):

        return self.remember(
            "opportunities",
            opportunity
        )



    def remember_execution(
        self,
        execution
    ):

        return self.remember(
            "executions",
            execution
        )



    def remember_worker(
        self,
        worker
    ):

        return self.remember(
            "workers",
            worker
        )



    def remember_improvement(
        self,
        improvement
    ):

        return self.remember(
            "improvements",
            improvement
        )



    def intelligence_report(self):

        from core.genesis.persistent_memory_core import (
            genesis_persistent_memory_core
        )

        memory = (
            genesis_persistent_memory_core
            .report()
        )


        return {

            "system":
                self.system,

            "memory":
                memory,

            "timestamp":
                time.time()

        }



genesis_memory_integration_layer = (
    GenesisMemoryIntegrationLayer()
)
