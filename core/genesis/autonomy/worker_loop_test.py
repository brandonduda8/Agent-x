from core.genesis.autonomy.worker_loop import (
    worker_loop
)


print("=" * 60)
print("♻️ GENESIS AUTONOMOUS WORKER LOOP TEST")
print("=" * 60)


result = worker_loop.run(
    "Acquire first AI automation customers"
)


print(result)


print(
    worker_loop.report()
)
