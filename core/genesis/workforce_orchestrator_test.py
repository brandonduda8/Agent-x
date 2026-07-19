from core.genesis.workforce_orchestrator import workforce_orchestrator


result = workforce_orchestrator.create_workforce(

    "Build customer acquisition system",

    [
        "coding",
        "sales",
        "crm",
        "marketing_analytics"
    ],

    [
        "coding",
        "sales",
        "crm"
    ]

)


print(result)

print(
    workforce_orchestrator.report()
)
