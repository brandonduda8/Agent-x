from core.genesis.genesis_outreach_execution_engine import outreach_engine


packets = [

    (
        "employment",
        "Immediate hiring employers",
        "Outreach Agent"
    ),

    (
        "employment",
        "Remote customer support applications",
        "Outreach Agent"
    ),

    (
        "revenue",
        "Dental clinics needing AI receptionist automation",
        "Revenue Agent"
    ),

    (
        "revenue",
        "Small businesses needing workflow automation",
        "Revenue Agent"
    ),

    (
        "housing",
        "Housing assistance programs",
        "Stability Agent"
    )

]


for p in packets:
    print(
        outreach_engine.create_packet(
            p[0],
            p[1],
            p[2]
        )
    )


print(outreach_engine.status())
