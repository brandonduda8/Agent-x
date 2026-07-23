import time
import uuid

from core.genesis.intelligence_router import intelligence_router


class SmartAgentExecutor:


    def __init__(self):

        self.system = "GENESIS SMART AGENT EXECUTOR v2"

        self.executions = []



    def detect_capability(
        self,
        agent
    ):

        if isinstance(agent, dict):

            role = agent.get(
                "role",
                ""
            )

            capability = agent.get(
                "capability",
                ""
            )

            skills = agent.get(
                "skills",
                []
            )

        else:

            role = getattr(
                agent,
                "role",
                ""
            )

            capability = getattr(
                agent,
                "capability",
                ""
            )

            skills = getattr(
                agent,
                "skills",
                [])


        text = (
            str(role)
            + " "
            + str(capability)
            + " "
            + " ".join(
                skills
            )
        ).lower()


        if any(
            word in text
            for word in [
                "code",
                "python",
                "automation",
                "debug"
            ]
        ):
            return "coding"


        if any(
            word in text
            for word in [
                "research",
                "analysis",
                "market"
            ]
        ):
            return "research"


        if any(
            word in text
            for word in [
                "sales",
                "revenue",
                "outreach",
                "client"
            ]
        ):
            return "revenue"


        return "general"



    def execute(
        self,
        agent,
        objective
    ):


        capability = self.detect_capability(
            agent
        )


        route = intelligence_router.select_models(
            capability
        )


        name = (
            agent.get("name")
            if isinstance(agent, dict)
            else agent.name
        )


        execution = {

            "id":
                "smart_"
                + uuid.uuid4().hex[:8],

            "agent":
                name,

            "capability":
                capability,

            "objective":
                objective,

            "models":
                route["models"],

            "status":
                "COMPLETE",

            "created":
                time.time()

        }


        self.executions.append(
            execution
        )


        print(
            "🤖 Smart Execution Complete:",
            name
        )


        return execution



    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(
                    self.executions
                )

        }



smart_agent_executor = SmartAgentExecutor()
