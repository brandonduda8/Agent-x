import time


class GenesisModelRegistry:


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
                    "research",
                    "planning"
                ],

                "status":
                "AVAILABLE"
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
                ],

                "status":
                "AVAILABLE"
            },


            {
                "name":
                "Free General Model",

                "provider":
                "OpenRouter",

                "tier":
                "FREE",

                "capabilities":
                [
                    "chat",
                    "simple_tasks"
                ],

                "status":
                "AVAILABLE"
            }

        ]



    def list_models(self):

        return self.models
