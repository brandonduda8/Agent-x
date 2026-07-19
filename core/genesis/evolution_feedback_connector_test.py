from core.genesis.evolution_feedback_connector import (
    evolution_feedback_connector
)


learning = {

    "mission":
        "Acquire first AI automation customers",

    "performance":
        1.0,

    "lesson":
        "Scale customer outreach workflow"

}


result = evolution_feedback_connector.process_learning(
    learning
)


print(result)

print()

print(
    evolution_feedback_connector.report()
)
