from core.genesis.meta.recursive_improvement_controller import (
    recursive_improvement_controller
)


print("=" * 60)
print("♻️ GENESIS RECURSIVE IMPROVEMENT CONTROLLER TEST")
print("=" * 60)


result = recursive_improvement_controller.improve(

    "Acquire AI automation customers",

    1.0,

    5000,

    "Lead Generation Agent"

)


print(result)

print(
    recursive_improvement_controller.report()
)
