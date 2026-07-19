import time
import uuid


class GenesisCEOIntelligence:

    """
    GENESIS CEO INTELLIGENCE ENGINE v1

    Responsible for:
    - understanding objectives
    - selecting agents
    - creating strategies
    - producing mission plans
    """

    def __init__(
        self,
        agent_registry=None,
        intelligence_mesh=None,
        event_stream=None
    ):

        self.system = "GENESIS CEO INTELLIGENCE ENGINE v1"

        self.agent_registry = agent_registry
        self.mesh = intelligence_mesh
        self.event_stream = event_stream

        self.decisions = []


    def analyze_objective(self, objective):

        objective_lower = objective.lower()

        agents = []


        if any(word in objective_lower for word in [
            "customer",
            "lead",
            "sales",
            "revenue",
            "money"
        ]):
            agents.append("Revenue")

            agents.append("Researcher")


        if any(word in objective_lower for word in [
            "build",
            "code",
            "software",
            "app"
        ]):
            agents.append("Builder")
            agents.append("Agent-X")


        if not agents:
            agents = [
                "Builder",
                "Researcher",
                "Revenue"
            ]


        decision = {

            "id":
                "decision_" + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "selected_agents":
                agents,

            "strategy":
                self.create_strategy(
                    objective,
                    agents
                ),

            "timestamp":
                time.time()
        }


        self.decisions.append(decision)


        if self.event_stream:
            self.event_stream.emit(
                "CEO_DECISION_CREATED",
                self.system,
                decision
            )


        return decision



    def create_strategy(
        self,
        objective,
        agents
    ):

        return {

            "objective":
                objective,

            "phases":[

                {
                    "phase":
                        "Research",

                    "agent":
                        "Researcher"
                },

                {
                    "phase":
                        "Execution",

                    "agents":
                        agents
                },

                {
                    "phase":
                        "Measurement",

                    "agent":
                        "Revenue"
                }

            ]
        }



    def report(self):

        return {

            "system":
                self.system,

            "decisions":
                len(self.decisions),

            "timestamp":
                time.time()
        }
