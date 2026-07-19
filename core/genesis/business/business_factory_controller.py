import time


from core.genesis.business.business_registry import (
    business_registry
)

from core.genesis.business.portfolio_intelligence import (
    portfolio_intelligence
)



class GenesisBusinessFactoryController:


    def __init__(self):

        self.system = (
            "GENESIS BUSINESS FACTORY CONTROLLER v1"
        )


    def create_business(
        self,
        opportunity
    ):


        print(
            "🏗️ Building autonomous company"
        )


        business = (
            business_registry.register_business(

                name=
                opportunity["market"]
                +
                " AI Automation Company",

                market=
                opportunity["market"],

                opportunity_value=
                opportunity["estimated_value"],

                agents=
                [
                "Sales Agent",
                "Lead Generation Agent",
                "Automation Agent",
                "Coding Agent",
                "CRM Agent",
                "Deployment Agent"
                ]

            )
        )


        analysis = (
            portfolio_intelligence.analyze(
                business_registry.list_businesses()
            )
        )


        return {

            "business":
            business,

            "portfolio":
            analysis,

            "status":
            "CREATED",

            "timestamp":
            time.time()

        }



business_factory_controller = (
    GenesisBusinessFactoryController()
)
