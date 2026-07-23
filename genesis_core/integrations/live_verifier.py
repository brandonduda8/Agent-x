import time

from genesis_core.config.env_loader import GenesisEnvironment


class GenesisLiveVerifier:


    def __init__(self):

        self.env = GenesisEnvironment()



    def verify_service(self, name, key):

        value = self.env.get(key)

        if value:

            return {

                "service": name,

                "status": "READY",

                "message": "Configuration detected"

            }


        return {

            "service": name,

            "status": "NOT_CONFIGURED",

            "message": "Missing configuration"

        }



    def run(self):

        return {

            "system":
            "GENESIS LIVE CONNECTION VERIFIER v1",

            "checks":

            [

                self.verify_service(
                    "OpenRouter",
                    "OPENROUTER_API_KEY"
                ),

                self.verify_service(
                    "Telegram",
                    "TELEGRAM_BOT_TOKEN"
                ),

                self.verify_service(
                    "Stripe",
                    "STRIPE_SECRET_KEY"
                )

            ],

            "timestamp":
            time.time()

        }



if __name__ == "__main__":

    verifier = GenesisLiveVerifier()

    print(
        verifier.run()
    )
