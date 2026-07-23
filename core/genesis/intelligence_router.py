import time


class GenesisIntelligenceRouter:


    def __init__(self):

        self.system = "GENESIS INTELLIGENCE ROUTER v1"

        self.routes = {

            "coding": [
                "deepseek/deepseek-coder",
                "qwen/qwen-coder",
                "codellama"
            ],

            "research": [
                "deepseek/deepseek-chat",
                "qwen/qwen-instruct",
                "llama-3"
            ],

            "revenue": [
                "qwen/qwen-instruct",
                "llama-3",
                "deepseek-chat"
            ],

            "planning": [
                "deepseek-reasoner",
                "qwen-reasoning",
                "llama-3"
            ],

            "general": [
                "llama-3",
                "qwen"
            ]

        }

        self.decisions = []



    def select_models(
        self,
        task_type
    ):

        models = self.routes.get(
            task_type.lower(),
            self.routes["general"]
        )


        decision = {

            "task":
                task_type,

            "models":
                models,

            "timestamp":
                time.time()

        }


        self.decisions.append(
            decision
        )


        print(
            "🧠 Intelligence Route:",
            task_type
        )

        print(
            "🤖 Models:",
            models
        )


        return decision



    def report(self):

        return {

            "system":
                self.system,

            "decisions":
                len(
                    self.decisions
                ),

            "routes":
                len(
                    self.routes
                )

        }



intelligence_router = GenesisIntelligenceRouter()
