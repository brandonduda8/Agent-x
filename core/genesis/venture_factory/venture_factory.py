import time
import uuid

from core.genesis.venture_factory.venture_builder import (
    venture_builder
)

from core.genesis.venture_factory.company_launcher import (
    company_launcher
)

from core.genesis.venture_factory.resource_allocator import (
    resource_allocator
)


class VentureFactory:

    def __init__(self):

        self.system = "GENESIS VENTURE FACTORY v1"
        self.ventures = []


    def create(self, opportunity):

        print(
            "🏭 Genesis Venture Factory activated"
        )


        venture = venture_builder.build(
            opportunity
        )


        company = company_launcher.launch(
            venture
        )


        resources = resource_allocator.allocate(
            company
        )


        result = {
            "id":
            "venture_cycle_" + uuid.uuid4().hex[:8],

            "venture": venture,

            "company": company,

            "resources": resources,

            "status": "LAUNCHED",

            "timestamp": time.time()
        }


        self.ventures.append(result)


        print(
            "🚀 Autonomous venture launched"
        )


        return result


venture_factory = VentureFactory()
