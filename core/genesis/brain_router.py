import time
import uuid


class GenesisBrainRouter:

    def __init__(self):

        self.name = "GENESIS BRAIN ROUTER v1"

        self.routes = {

            "coding": [
                "coding-model",
                "python-agent"
            ],

            "research": [
                "research-model",
                "analysis-agent"
            ],

            "revenue": [
                "sales-model",
                "marketing-agent"
            ],

            "automation": [
                "automation-model",
                "workflow-agent"
            ],

            "general": [
                "general-model"
            ]

        }

        self.history = []



    def classify_task(
        self,
        objective
    ):

        text = objective.lower()


        if any(
            word in text
            for word in [
                "code",
                "python",
                "software",
                "build",
                "api",
                "agent"
            ]
        ):

            return "coding"


        if any(
            word in text
            for word in [
                "research",
                "find",
                "analyze",
                "search"
            ]
        ):

            return "research"


        if any(
            word in text
            for word in [
                "sell",
                "client",
                "customer",
                "revenue",
                "money"
            ]
        ):

            return "revenue"


        if any(
            word in text
            for word in [
                "automation",
                "workflow",
                "system"
            ]
        ):

            return "automation"


        return "general"



    def route(
        self,
        objective
    ):

        category = (
            self.classify_task(
                objective
            )
        )


        selected_models = (
            self.routes[
                category
            ]
        )


        decision = {

            "id":
                "brain_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "category":
                category,

            "models":
                selected_models,

            "timestamp":
                time.time()

        }


        self.history.append(
            decision
        )


        print(
            "🧠 Genesis Brain Decision:"
        )

        print(
            "   Category:",
            category
        )

        print(
            "   Models:",
            selected_models
        )


        return decision



    def learn_model_result(
        self,
        model,
        score
    ):

        from core.genesis.genesis_memory import (
            genesis_memory
        )


        genesis_memory.store_model_result(
            model,
            score
        )



    def report(
        self
    ):

        return {

            "system":
                self.name,

            "routes":
                len(
                    self.routes
                ),

            "decisions":
                len(
                    self.history
                ),

            "timestamp":
                time.time()

        }



brain_router = GenesisBrainRouter()
