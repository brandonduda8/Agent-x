import os


class OpenRouterAdapter:


    def check(self):

        key = os.getenv(
            "OPENROUTER_API_KEY"
        )


        if key:

            return {

                "name":
                "OpenRouter",

                "status":
                "CONFIGURED"

            }


        return {

            "name":
            "OpenRouter",

            "status":
            "MISSING_KEY"

        }
