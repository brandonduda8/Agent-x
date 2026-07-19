from core.genesis.business_automation_engine import business_automation_engine


opp = business_automation_engine.create_opportunity(

    "AI Automation Service",

    "Small Business",

    0.92,

    "Revenue Intelligence Agent"

)


print(opp)


workflow = business_automation_engine.create_workflow(

    opp["id"],

    [
        "Research customer",
        "Generate offer",
        "Create outreach",
        "Track response"
    ],

    "Genesis Sales Agent"

)


print(workflow)


print(

business_automation_engine.record_revenue_event(

    "AI Automation Service",

    1000

)

)


print(
    business_automation_engine.status()
)
