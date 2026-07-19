from core.genesis.research.autonomous_business_creator import (
    autonomous_business_creator
)


print("="*60)
print("🏗️ GENESIS AUTONOMOUS BUSINESS CREATOR TEST")
print("="*60)


opportunity = {

    "id":"opportunity_demo",

    "market":"Healthcare AI",

    "score":90,

    "estimated_value":5000

}


result = autonomous_business_creator.create(
    opportunity
)


print(result)
