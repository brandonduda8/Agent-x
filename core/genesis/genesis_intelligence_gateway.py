import time
import uuid


from core.genesis.intelligence_router import (
    intelligence_router
)

from core.genesis.smart_agent_executor import (
    smart_agent_executor
)

from core.genesis.llm_connector import (
    llm_connector
)


try:
    from core.genesis.persistent_memory_core import (
        genesis_persistent_memory_core
    )
except Exception:
    genesis_persistent_memory_core = None


class GenesisIntelligenceGateway:

    """
    GENESIS INTELLIGENCE GATEWAY v1

    Executive coordination layer.

    Responsibilities:

    - analyze missions
    - select capability
    - select models
    - execute through agents
    - remember outcomes
    """

    def __init__(self):

        self.system = (
            "GENESIS INTELLIGENCE GATEWAY v1"
        )

        self.decisions = []

        self.executions = []


    def classify_task(
        self,
        mission
    ):

        text = str(
            mission
        ).lower()


        if any(
            x in text
            for x in [
                "code",
                "python",
                "build",
                "debug",
                "software",
                "api"
            ]
        ):
            return "coding"


        if any(
            x in text
            for x in [
                "money",
                "sales",
                "client",
                "revenue",
                "lead"
            ]
        ):
            return "revenue"


        if any(
            x in text
            for x in [
                "research",
                "analyze",
                "study",
                "market"
            ]
        ):
            return "research"


        return "general"



    def execute(
        self,
        mission,
        agent
    ):


        capability = self.classify_task(
            mission
        )


        model_route = (
            intelligence_router
            .select_models(
                capability
            )
        )


        llm_plan = (
            llm_connector
            .run(
                capability,
                mission
            )
        )


        execution = {

            "id":
                "gateway_"
                +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "agent":
                agent,

            "capability":
                capability,

            "models":
                model_route["models"],

            "llm":
                llm_plan,

            "status":
                "READY",

            "timestamp":
                time.time()

        }


        self.executions.append(
            execution
        )


        self.decisions.append(
            execution
        )


        if genesis_persistent_memory_core:

            try:

                genesis_persistent_memory_core.remember(
                    "gateway_decisions",
                    execution
                )

            except Exception:

                pass


        print(
            "🧠 Gateway Execution:",
            capability
        )


        return execution



    def report(self):

        return {

            "system":
                self.system,

            "decisions":
                len(
                    self.decisions
                ),

            "executions":
                len(
                    self.executions
                ),

            "timestamp":
                time.time()

        }



genesis_intelligence_gateway = (
    GenesisIntelligenceGateway()
)
