from core.genesis.memory.learning_memory_connector import (
    learning_memory_connector
)


print("=" * 50)
print("🔁 GENESIS LEARNING MEMORY CONNECTOR TEST")
print("=" * 50)


result = learning_memory_connector.store_learning(
    "Revenue Agent",
    {
        "mission":
        "Acquire first AI automation customers",

        "performance":
        1.0,

        "lesson":
        "Personalized outreach improves conversion"
    }
)


print(result)

print(
    learning_memory_connector.report()
)
