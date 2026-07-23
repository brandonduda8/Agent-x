import time

from core.genesis.genesis_reality_action_executor import action_executor

print({
    "system": "GENESIS REALITY WORKER LOOP v1",
    "status": "STARTING",
    "message": "Converting created actions into execution cycles",
    "timestamp": time.time()
})

actions = action_executor.status()["actions"]

for action in actions:
    if action["status"] == "CREATED":

        result = {
            "action_id": action["id"],
            "agent": action["agent"],
            "category": action["category"],
            "objective": action["objective"],
            "execution_status": "DISPATCHED",
            "next_step": "COLLECT REAL WORLD RESULT"
        }

        print(result)

print({
    "system": "GENESIS REALITY WORKER LOOP v1",
    "status": "ONLINE",
    "dispatched_actions": len(actions),
    "timestamp": time.time()
})
