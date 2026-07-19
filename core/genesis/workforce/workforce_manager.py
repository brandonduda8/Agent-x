import time


from core.genesis.workforce.agent_registry import (
    agent_registry
)

from core.genesis.workforce.performance_ranker import (
    performance_ranker
)

from core.genesis.workforce.promotion_engine import (
    promotion_engine
)



class GenesisWorkforceManager:


    def __init__(self):

        self.system = "GENESIS WORKFORCE MANAGER v1"



    def onboard(
        self,
        name,
        skills,
        performance
    ):


        agent = agent_registry.register(
            name,
            skills
        )


        agent_registry.update_performance(
            name,
            performance
        )


        agent = performance_ranker.rank(
            agent
        )


        promotion = promotion_engine.evaluate(
            agent
        )


        return {

            "agent":agent,

            "promotion":promotion,

            "timestamp":time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "registry":
            agent_registry.report(),

            "ranker":
            performance_ranker.report(),

            "promotion":
            promotion_engine.report()

        }



workforce_manager = GenesisWorkforceManager()
