from core.genesis.business_creator.creator_brain import (
    creator_brain
)


print("=" * 60)
print("🧬 GENESIS AUTONOMOUS BUSINESS CREATOR TEST")
print("=" * 60)


result = creator_brain.create()


print(result)


print({
"system":
"GENESIS AUTONOMOUS BUSINESS CREATOR v2",
"cycles":
len(creator_brain.cycles)
})
