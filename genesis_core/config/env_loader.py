import os
from pathlib import Path


class GenesisEnvironmentLoader:


    def load(self):

        env_path = Path(".env")


        if env_path.exists():

            with open(env_path) as file:

                for line in file:

                    line=line.strip()

                    if (
                        line
                        and
                        not line.startswith("#")
                        and
                        "=" in line
                    ):

                        key,value=line.split(
                            "=",
                            1
                        )

                        os.environ[key]=value


        return {

            "OPENROUTER_API_KEY":
            self.exists("OPENROUTER_API_KEY"),

            "TELEGRAM_BOT_TOKEN":
            self.exists("TELEGRAM_BOT_TOKEN"),

            "STRIPE_SECRET_KEY":
            self.exists("STRIPE_SECRET_KEY")

        }



    def exists(
        self,
        key
    ):

        return bool(
            os.getenv(key)
        )
