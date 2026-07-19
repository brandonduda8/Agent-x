print("="*60)
print("♻️ GENESIS AUTONOMOUS LOOP TEST")
print("="*60)


from core.genesis.autonomy.autonomous_loop import (
    autonomous_loop
)


result = autonomous_loop.run(
    "Acquire first AI automation customers",
    "Healthcare AI Automation Company",
    "Healthcare AI"
)


print(result)

print(
    autonomous_loop.report()
)
