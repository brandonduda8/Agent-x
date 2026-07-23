import time


class GenesisLLMRouter:

    def __init__(
        self,
        model_registry=None
    ):

        self.system = "GENESIS LLM ROUTER v2"

        self.model_registry = model_registry

        self.requests = 0



    def classify_task(
        self,
        task
    ):

        text = task.lower()


        if any(
            x in text
            for x in [
                "code",
                "python",
                "api",
                "software",
                "debug"
            ]
        ):

            return "coding"


        if any(
            x in text
            for x in [
                "research",
                "market",
                "analyze",
                "study"
            ]
        ):

            return "research"



        if any(
            x in text
            for x in [
                "plan",
                "strategy",
                "architecture"
            ]
        ):

            return "reasoning"


        return "cheap"



    def request_model(
        self,
        task
    ):

        category = self.classify_task(task)


        self.requests += 1


        models = []


        if self.model_registry:

            models = self.model_registry.get_models(
                category
            )


        return {

            "task":
                task,

            "category":
                category,

            "available_models":
                models,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "requests":
                self.requests,

            "timestamp":
                time.time()

        }


try:

    from core.genesis.llm.model_registry import model_registry

    llm_router = GenesisLLMRouter(
        model_registry
    )

except:

    llm_router = GenesisLLMRouter()
