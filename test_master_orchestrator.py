
from genesis_core.orchestrator.master_orchestrator import GenesisMasterOrchestrator
from genesis_core.economics.economic_os import GenesisEconomicOS
from genesis_core.actions.action_fabric import GenesisActionFabric
from genesis_core.memory.memory_fabric import GenesisMemoryFabric


class SimpleOptimizer:

    def create_mission(self, opportunity):

        return {

            "mission":
            opportunity["name"],

            "status":
            "READY"

        }



economic = GenesisEconomicOS()

actions = GenesisActionFabric()

memory = GenesisMemoryFabric()

optimizer = SimpleOptimizer()


genesis = GenesisMasterOrchestrator(

    economic,

    optimizer,

    actions,

    memory

)


result = genesis.run({

    "name":
    "Dental AI Reception Automation",

    "category":
    "business",

    "value":
    999

})


print(result)

print(
genesis.status()
)

print(
economic.dashboard()
)

print(
actions.status()
)

print(
memory.summarize()
)

