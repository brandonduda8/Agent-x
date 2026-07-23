import time
import uuid

from core.genesis.capability_analyzer import (
    genesis_capability_analyzer
)

from core.genesis.intelligence_router import (
    intelligence_router
)

from core.genesis.llm_connector import (
    llm_connector
)


class GenesisIntelligenceGatewayV2:


    def __init__(self):

        self.system = (
            "GENESIS INTELLIGENCE GATEWAY v2"
        )

        self.executions = []



    def execute(
        self,
        mission,
        agent
    ):


        capability = (
            genesis_capability_analyzer.analyze(
                mission
            )
        )


        route = (
            intelligence_router.select_models(
                capability["capability"]
            )
        )


        llm = (
            llm_connector.run(
                capability["capability"],
                mission
            )
        )


        result = {

            "id":
            "gateway_v2_"
            +
            uuid.uuid4().hex[:8],

            "mission":
            mission,

            "agent":
            agent,

            "capability":
            capability,

            "models":
            route["models"],

            "llm":
            llm,

            "status":
            "READY",

            "timestamp":
            time.time()

        }


        self.executions.append(
            result
        )


        print(
            "🚀 Gateway v2 execution:",
            capability["capability"]
        )


        return result



    def report(self):

        return {

            "system":
            self.system,

            "executions":
            len(self.executions),

            "timestamp":
            time.time()

        }



genesis_intelligence_gateway_v2 = (
    GenesisIntelligenceGatewayV2()
)
