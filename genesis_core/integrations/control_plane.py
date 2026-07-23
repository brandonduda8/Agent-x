from genesis_core.integrations.registry import GenesisIntegrationRegistry

from genesis_core.integrations.adapters.openrouter_adapter import OpenRouterAdapter
from genesis_core.integrations.adapters.telegram_adapter import TelegramAdapter
from genesis_core.integrations.adapters.stripe_adapter import StripeAdapter



class GenesisControlPlane:


    def __init__(self):

        self.registry = GenesisIntegrationRegistry()



    def verify(self):

        adapters = [

            OpenRouterAdapter(),

            TelegramAdapter(),

            StripeAdapter()

        ]


        for adapter in adapters:

            result = adapter.check()

            self.registry.register(

                result["name"],

                result["status"]

            )


        return self.registry.report()



if __name__ == "__main__":

    plane = GenesisControlPlane()

    print(
        plane.verify()
    )
