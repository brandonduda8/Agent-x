from core.genesis.learning.learning_extractor import (
    learning_extractor
)

from core.genesis.learning.knowledge_graph import (
    knowledge_graph
)

from core.genesis.learning.skill_transfer_engine import (
    skill_transfer_engine
)


print("=" * 60)
print("🧠 GENESIS META-LEARNING ENGINE TEST")
print("=" * 60)


lesson = learning_extractor.extract(
    "Acquire AI automation customers",
    1.0,
    {
        "sales_success": True,
        "revenue": 5000
    }
)


knowledge = knowledge_graph.store(
    lesson
)


transfer = skill_transfer_engine.transfer(
    knowledge,
    "Future Sales Agent"
)


print(lesson)
print(knowledge)
print(transfer)

print(
    learning_extractor.report()
)

print(
    knowledge_graph.report()
)

print(
    skill_transfer_engine.report()
)
