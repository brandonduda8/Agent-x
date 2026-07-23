import os
import time


class GenesisConfigManager:


    def __init__(self):

        self.services = {

            "OpenRouter": {
                "env":
                "OPENROUTER_API_KEY"
            },

            "Telegram": {
                "env":
                "TELEGRAM_BOT_TOKEN"
            },

            "Stripe": {
                "env":
                "STRIPE_SECRET_KEY"
            }

        }



    def check_service(
        self,
        name
    ):

        service = self.services.get(
            name
        )

        if not service:

            return {

                "service":
                name,

                "status":
                "UNKNOWN"

            }


        value = os.getenv(
            service["env"]
        )


        return {

            "service":
            name,

            "status":
            "CONFIGURED"
            if value
            else
            "MISSING",

            "timestamp":
            time.time()

        }



    def check_all(self):

        return [

            self.check_service(name)

            for name in self.services

        ]
