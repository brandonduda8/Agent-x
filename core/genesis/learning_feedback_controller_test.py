from core.genesis.learning_feedback_controller import (
    learning_feedback_controller
)


execution = {

    "mission":
        "Acquire first AI automation customers",

    "results":

    [

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


result = learning_feedback_controller.process_execution(
    execution
)


print(result)

print()

print(
    learning_feedback_controller.report()
)
