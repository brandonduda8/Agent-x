import time
import uuid


class GenesisModelRouter:


    def __init__(self):

        self.models = [

            {

            "name":
            "Free Reasoning Model",

            "provider":
            "OpenRouter",

            "tier":
            "FREE",

            "capabilities":

                [

                "reasoning",

                "planning",

                "analysis"

                ]

            },


            {

            "name":
            "Free Coding Model",

            "provider":
            "OpenRouter",

            "tier":
            "FREE",

            "capabilities":

                [

                "coding",

                "debugging",

                "engineering"

                ]

            },


            {

            "name":
            "Free Research Model",

            "provider":
            "OpenRouter",

            "tier":
            "FREE",

            "capabilities":

                [

                "research",

                "analysis",

                "search"

                ]

            }

        ]



        self.history = []



    def select_model(
        self,
        capability
    ):


        matches = []


        for model in self.models:

            if capability in model["capabilities"]:

                matches.append(model)



        if not matches:

            selected = self.models[0]

        else:

            selected = matches[0]



        result = {


            "id":
            "model_route_" + uuid.uuid4().hex[:8],


            "capability":
            capability,


            "selected_model":
            selected,


            "timestamp":
            time.time()

        }


        self.history.append(
            result
        )


        return result



    def status(self):

        return {


            "system":
            "GENESIS DYNAMIC MODEL ROUTER v1",


            "available_models":
            len(self.models),


            "routes_created":
            len(self.history),


            "timestamp":
            time.time()

        }
