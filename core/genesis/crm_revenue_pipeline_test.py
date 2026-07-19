from core.genesis.crm_revenue_pipeline_engine import (
    crm_revenue_pipeline_engine
)


print("=" * 60)
print("💰 GENESIS CRM REVENUE PIPELINE TEST")
print("=" * 60)


contact = crm_revenue_pipeline_engine.create_contact(
    "Healthcare AI Company"
)


deal = crm_revenue_pipeline_engine.create_deal(
    contact,
    "AI automation consulting and implementation package"
)


crm_revenue_pipeline_engine.update_stage(
    deal,
    "OUTREACH_SENT"
)


crm_revenue_pipeline_engine.update_stage(
    deal,
    "MEETING_BOOKED"
)


crm_revenue_pipeline_engine.update_stage(
    deal,
    "PROPOSAL_SENT"
)


revenue = crm_revenue_pipeline_engine.record_revenue(
    deal,
    5000
)


print(revenue)

print(
    crm_revenue_pipeline_engine.pipeline_report()
)
