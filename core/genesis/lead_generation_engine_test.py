from core.genesis.lead_generation_engine import lead_generation_engine


lead = lead_generation_engine.create_lead(

    "Local Business",

    "Services",

    "AI automation",

    0.88,

    "Research Agent"

)


print(lead)

print(
    lead_generation_engine.qualify_lead(
        lead["id"]
    )
)


print(
    lead_generation_engine.status()
)
