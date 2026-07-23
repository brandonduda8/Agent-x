import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "operator": {},
            "agents": {},
            "missions": [],
            "results": [],
            "decisions": []
        }

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def register_agent(name, category):
    memory = load_memory()

    memory["agents"][name] = {
        "category": category,
        "status": "ONLINE",
        "last_update": str(datetime.now())
    }

    save_memory(memory)


def create_mission(agent, objective):
    memory = load_memory()

    mission = {
        "agent": agent,
        "objective": objective,
        "status": "DISPATCHED",
        "created": str(datetime.now())
    }

    memory["missions"].append(mission)

    save_memory(memory)


def add_result(agent, result):
    memory = load_memory()

    memory["results"].append({
        "agent": agent,
        "result": result,
        "timestamp": str(datetime.now())
    })

    save_memory(memory)


if __name__ == "__main__":

    register_agent(
        "Opportunity Discovery Agent",
        "income"
    )

    register_agent(
        "Revenue Agent",
        "revenue"
    )

    register_agent(
        "Stability Agent",
        "housing"
    )

    create_mission(
        "Opportunity Discovery Agent",
        "Find income opportunities"
    )

    create_mission(
        "Revenue Agent",
        "Find business leads"
    )

    create_mission(
        "Stability Agent",
        "Find housing resources"
    )

    add_result(
        "Genesis Core",
        "Memory system online"
    )

    print("GENESIS CORE ONLINE")
