import os
import sys
import time


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if ROOT not in sys.path:
    sys.path.insert(
        0,
        ROOT
    )


from core.genesis.runtime_registry import (
    runtime_registry
)

from genesis_core.economics.economic_os import (
    GenesisEconomicOS
)

from genesis_core.revenue.revenue_engine import (
    GenesisRevenueEngine
)

from genesis_core.crm.crm import (
    GenesisCRM
)

from genesis_core.revenue.genesis_revenue_mission_controller import (
    GenesisRevenueMissionController
)

from genesis_core.memory.state_hydrator import (
    GenesisStateHydrator
)

from genesis_core.memory.database import (
    GenesisDatabase
)



class GenesisRevenueFusionAdapter:


    def __init__(
        self,
        event_bus=None
    ):

        self.system = (
            "GENESIS REVENUE FUSION ADAPTER v3"
        )

        self.event_bus = event_bus


        self.economic = (
            runtime_registry.get("economic")
            or runtime_registry.register(
                "economic",
                GenesisEconomicOS()
            )
        )


        self.revenue = (
            runtime_registry.get("revenue")
            or runtime_registry.register(
                "revenue",
                GenesisRevenueEngine()
            )
        )


        self.crm = (
            runtime_registry.get("crm")
            or runtime_registry.register(
                "crm",
                GenesisCRM()
            )
        )


        self.controller = (
            runtime_registry.get(
                "revenue_controller"
            )
            or runtime_registry.register(
                "revenue_controller",
                GenesisRevenueMissionController(
                    self.economic,
                    self.revenue,
                    self.crm,
                    self.event_bus
                )
            )
        )


        self.hydrator = GenesisStateHydrator(
            GenesisDatabase()
        )


        self.hydration = (
            self.hydrator.hydrate(
                self.economic,
                self.revenue
            )
        )



    def activate_offer(
        self,
        business,
        industry,
        problem,
        offer,
        value
    ):

        return (
            self.controller.create_revenue_mission(
                business,
                industry,
                problem,
                offer,
                value
            )
        )



    def dashboard(self):

        return {

            "system":
            self.system,

            "hydration":
            self.hydration,

            "runtime":
            runtime_registry.report(),

            "economic":
            self.economic.dashboard(),

            "revenue":
            self.revenue.report(),

            "crm":
            self.crm.pipeline(),

            "missions":
            self.controller.report(),

            "timestamp":
            time.time()

        }



genesis_revenue_fusion_adapter = (
    GenesisRevenueFusionAdapter()
)
