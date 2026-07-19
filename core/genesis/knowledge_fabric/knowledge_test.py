from core.genesis.knowledge_fabric.knowledge_brain import (
    knowledge_brain
)


print("=" * 60)
print("🧬 GENESIS KNOWLEDGE FABRIC TEST")
print("=" * 60)


result = knowledge_brain.execute()


print(result)


print({
"system":
"GENESIS KNOWLEDGE FABRIC v1",
"cycles":
len(knowledge_brain.cycles)
})
