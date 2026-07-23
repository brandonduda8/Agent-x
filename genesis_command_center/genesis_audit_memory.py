import json
from datetime import datetime
import os


MEMORY_FILE = "genesis_audit_log.json"


def load_memory():

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    return []


def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)



def record_event(agent, action, result, approval=False):

    memory = load_memory()

    event = {
        "id": len(memory) + 1,
        "timestamp": str(datetime.now()),
        "agent": agent,
        "action": action,
        "result": result,
        "approval_required": approval
    }

    memory.append(event)

    save_memory(memory)

    return event



system = {

    "system": "GENESIS AUDIT MEMORY ENGINE",

    "status": "ONLINE",

    "timestamp": str(datetime.now()),

    "recorded_event": record_event(
        "Genesis Core",
        "Connected executive memory layer",
        "Audit tracking enabled",
        False
    ),

    "memory_file": MEMORY_FILE

}


print(json.dumps(system, indent=4))
