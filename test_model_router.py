
from genesis_core.models.model_router import GenesisModelRouter


router = GenesisModelRouter()


tests = [

    "reasoning",

    "coding",

    "research"

]


for capability in tests:

    print(
        router.select_model(
            capability
        )
    )


print(
    router.status()
)

