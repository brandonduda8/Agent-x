from core.genesis.business.business_registry import (
    business_registry
)

from core.genesis.business.meta_ceo_portfolio_manager import (
    meta_ceo_portfolio_manager
)

from core.genesis.business.business_growth_engine import (
    business_growth_engine
)


print("="*60)
print("👑 GENESIS META CEO PORTFOLIO TEST")
print("="*60)


business = business_registry.register_business(

    "Healthcare AI Automation Company",

    "Healthcare AI",

    5000,

    [
        "Sales Agent",
        "Lead Generation Agent",
        "Automation Agent"
    ]

)


decision = (
    meta_ceo_portfolio_manager
    .evaluate_business(
        business
    )
)


upgrade = (
    business_growth_engine
    .generate_upgrade(
        business,
        decision
    )
)


print(
    {
        "decision": decision,
        "upgrade": upgrade
    }
)


print(
    meta_ceo_portfolio_manager.report()
)

print(
    business_growth_engine.report()
)
