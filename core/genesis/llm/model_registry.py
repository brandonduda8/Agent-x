import time


class GenesisModelRegistry:

    def __init__(self):

        self.system = "GENESIS MODEL REGISTRY v1"

        self.models = {

            "reasoning": [],

            "coding": [],

            "research": [],

            "cheap": []

        }


    def register_model(
        self,
        name,
        category,
        provider="unknown"
    ):

        model = {

            "name": name,

            "category": category,

            "provider": provider,

            "status": "AVAILABLE",

            "created": time.time()

        }


        if category not in self.models:

            self.models[category] = []


        self.models[category].append(model)


        print(
            f"🧠 Registered LLM: {name} -> {category}"
        )


        return model



    def get_models(
        self,
        category
    ):

        return self.models.get(
            category,
            []
        )


    def report(self):

        return {

            "system":
                self.system,

            "models":
                self.models,

            "timestamp":
                time.time()

        }


model_registry = GenesisModelRegistry()
