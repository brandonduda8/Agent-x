print("=" * 60)
print("🧠 GENESIS COGNITIVE CORE TEST")
print("=" * 60)


from core.genesis.cognitive.memory_cortex import memory_cortex
from core.genesis.cognitive.pattern_recognition import pattern_recognizer
from core.genesis.cognitive.decision_engine import decision_engine
from core.genesis.cognitive.agent_training_engine import agent_training_engine
from core.genesis.cognitive.knowledge_router import knowledge_router


memory = memory_cortex.store(
    "MISSION_RESULT",
    {
        "objective": "Acquire AI automation customers",
        "revenue": 5000,
        "success": True
    }
)


pattern = pattern_recognizer.analyze(memory)


decision = decision_engine.decide(
    "Scale AI automation business",
    pattern
)


training = agent_training_engine.train(
    "Sales Agent",
    pattern
)


transfer = knowledge_router.transfer(
    pattern,
    "Future Sales Agent"
)


print(memory)
print(pattern)
print(decision)
print(training)
print(transfer)


print(memory_cortex.report())
print(pattern_recognizer.report())
print(decision_engine.report())
print(agent_training_engine.report())
print(knowledge_router.report())
