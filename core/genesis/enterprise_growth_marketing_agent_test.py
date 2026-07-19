from core.genesis.enterprise_growth_marketing_agent import enterprise_growth_marketing_agent


opportunity = enterprise_growth_marketing_agent.discover_opportunity(
    "AI Automation Consulting Market",
    "Revenue",
    95,
    "Genesis Research Agent"
)


campaign = enterprise_growth_marketing_agent.create_campaign(
    opportunity["name"],
    "Multi Channel Outreach",
    "Acquire first 10 AI automation customers"
)


grant = enterprise_growth_marketing_agent.discover_grant(
    "AI Innovation Grant",
    "Technology Funding Program",
    90
)


partner = enterprise_growth_marketing_agent.create_partnership(
    "AI Software Company",
    "Strategic automation partnership"
)


print(opportunity)
print(campaign)
print(grant)
print(partner)

print(
    enterprise_growth_marketing_agent.growth_report()
)
