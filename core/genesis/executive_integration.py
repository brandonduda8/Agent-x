import time


class GenesisExecutiveIntegration:
    """
    GENESIS EXECUTIVE INTEGRATION LAYER v1

    Connects:
    - Executive Registry
    - LLM Router
    - Workforce Manager
    - Intelligence Graph
    - Skill Adapter

    Purpose:
    Give executive agents access to Genesis infrastructure.
    """

    def __init__(
        self,
        executive_registry=None,
        llm_router=None,
        workforce_manager=None,
        intelligence_graph=None,
        skill_adapter=None
    ):

        self.system = "GENESIS EXECUTIVE INTEGRATION LAYER v1"

        self.executive_registry = executive_registry
        self.llm_router = llm_router
        self.workforce_manager = workforce_manager
        self.intelligence_graph = intelligence_graph
        self.skill_adapter = skill_adapter

        self.executions = []


    def activate_executive(self, executive, objective):

        execution = {
            "executive": executive,
            "objective": objective,
            "llm": None,
            "workers": [],
            "knowledge": None,
            "skills": None,
            "status": "STARTING",
            "timestamp": time.time()
        }


        # Connect intelligence
        if self.intelligence_graph:
            try:
                execution["knowledge"] = (
                    self.intelligence_graph.add_node(
                        "objective",
                        objective,
                        {
                            "executive": executive
                        }
                    )
                )
            except Exception:
                pass


        # Connect skills
        if self.skill_adapter:
            try:
                execution["skills"] = (
                    self.skill_adapter.analyze_gap(
                        objective
                    )
                )
            except Exception:
                pass


        # Connect LLM routing
        if self.llm_router:
            try:
                category = "reasoning"

                text = objective.lower()

                if any(x in text for x in [
                    "code",
                    "software",
                    "python",
                    "api"
                ]):
                    category = "coding"

                elif any(x in text for x in [
                    "research",
                    "market",
                    "customer"
                ]):
                    category = "research"


                execution["llm"] = (
                    self.llm_router.route(
                        objective,
                        category
                    )
                )

            except Exception:
                pass


        # Connect workforce
        if self.workforce_manager:
            try:
                execution["workers"] = (
                    self.workforce_manager.report()
                )
            except Exception:
                pass


        execution["status"] = "READY"

        self.executions.append(execution)

        print(
            f"👑 Executive integrated: {executive}"
        )

        return execution



    def report(self):

        return {
            "system": self.system,
            "executions": len(self.executions),
            "timestamp": time.time()
        }


genesis_executive_integration = GenesisExecutiveIntegration()
