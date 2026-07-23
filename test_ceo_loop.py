
from genesis_core.ceo_loop.ceo_loop import GenesisCEOLoop
from genesis_core.optimizer.mission_optimizer import GenesisMissionOptimizer
from genesis_core.governance.meta_council import GenesisMetaGovernanceCouncil
from genesis_core.models.model_router import GenesisModelRouter


optimizer = GenesisMissionOptimizer()

council = GenesisMetaGovernanceCouncil()

council.register_agent(
    "Agent-X Coding Agent",
    "engineering",
    [
        "coding",
        "engineering",
        "deployment"
    ]
)


router = GenesisModelRouter()


ceo = GenesisCEOLoop(
    optimizer,
    council,
    router
)


result = ceo.execute_cycle({

"name":
"Dental AI Reception Automation",

"value":
999,

"urgency":
90,

"automation_fit":
95,

"speed":
85

})


print(result)


print(
ceo.status()
)

