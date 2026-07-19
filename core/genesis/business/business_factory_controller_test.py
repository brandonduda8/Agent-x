from core.genesis.business.business_factory_controller import (
    business_factory_controller
)


print("="*60)
print("🏭 GENESIS BUSINESS FACTORY TEST")
print("="*60)


opportunity = {

"id":
"opportunity_healthcare",

"market":
"Healthcare AI",

"estimated_value":
5000

}


result = (
    business_factory_controller
    .create_business(
        opportunity
    )
)


print(result)
