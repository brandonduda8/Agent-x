from core.genesis.revenue_execution_bridge import (
    revenue_execution_bridge
)


execution = {

    "results": [

        {
            "agent":
                "Revenue Agent",

            "capability":
                "sales",

            "result":
                "SUCCESS"

        },

        {
            "agent":
                "Coding Agent",

            "capability":
                "coding",

            "result":
                "SUCCESS"

        }

    ]

}


result = revenue_execution_bridge.process_execution(
    execution
)


print(result)

print()

print(
    revenue_execution_bridge.report()
)
