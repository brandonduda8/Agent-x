from core.genesis.meta.meta_ceo_controller import (
    meta_ceo_controller
)


print("=" * 60)
print("👑 GENESIS META CEO CONTROLLER TEST")
print("=" * 60)


result = meta_ceo_controller.run(

    "Acquire AI automation customers",

    1.0,

    5000,

    "Lead Generation Agent"

)


print(result)

print(
    meta_ceo_controller.report()
)
