import os
import time


class GenesisIntelligenceAdapterManager:

    def __init__(self):

        self.system = (
            "GENESIS INTELLIGENCE ADAPTER MANAGER v1"
        )


    def scan(self):

        adapters = {

            "openrouter": {
                "connected":
                    bool(
                        os.getenv(
                            "OPENROUTER_API_KEY"
                        )
                    )
            },

            "openai": {
                "connected":
                    bool(
                        os.getenv(
                            "OPENAI_API_KEY"
                        )
                    )
            }

        }


        return {

            "system":
                self.system,

            "adapters":
                adapters,

            "recommendation":
                self.recommendation(
                    adapters
                ),

            "timestamp":
                time.time()

        }


    def recommendation(self, adapters):

        connected = [
            name
            for name, data
            in adapters.items()
            if data["connected"]
        ]


        if connected:

            return (
                "Intelligence adapters online: "
                + ", ".join(connected)
            )


        return (
            "No external intelligence adapters connected"
        )


    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_intelligence_adapter_manager = (
    GenesisIntelligenceAdapterManager()
)
