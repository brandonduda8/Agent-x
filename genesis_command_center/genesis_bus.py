import json
import datetime
import os

MEMORY_FILE = "memory.json"


class GenesisBus:

    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)

        return {
            "events": [],
            "agents": {},
            "missions": [],
            "results": []
        }

    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=4)

    def emit(self, agent, action, payload=None):

        event = {
            "agent": agent,
            "action": action,
            "payload": payload,
            "timestamp": str(datetime.datetime.now()),
            "status": "EXECUTED"
        }

        self.memory.setdefault("events", []).append(event)

        self.save_memory()

        return event


    def register_agent(self, name, category):

        self.memory.setdefault("agents", {})[name] = {
            "category": category,
            "status": "ONLINE",
            "connected": True
        }

        self.save_memory()

        return self.memory["agents"][name]


    def dispatch(self, agent, mission):

        task = {
            "agent": agent,
            "mission": mission,
            "created": str(datetime.datetime.now()),
            "status": "DISPATCHED"
        }

        self.memory.setdefault("missions", []).append(task)

        self.save_memory()

        return task


if __name__ == "__main__":

    bus = GenesisBus()

    print(
        bus.emit(
            "Genesis Core",
            "Unified command bus online"
        )
    )

    bus.register_agent(
        "Opportunity Discovery Agent",
        "income"
    )

    bus.register_agent(
        "Revenue Agent",
        "revenue"
    )

    bus.register_agent(
        "Stability Agent",
        "housing"
    )

    print(
        bus.dispatch(
            "Genesis Core",
            "Coordinate all connected agents"
        )
    )
