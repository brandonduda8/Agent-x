import json
from datetime import datetime


models = [

    {
        "name": "OpenAI Reasoning Model",
        "provider": "OpenAI",
        "category": "reasoning",
        "tasks": [
            "planning",
            "decision intelligence",
            "executive summaries"
        ],
        "status": "AVAILABLE"
    },

    {
        "name": "Open Source Code Models",
        "provider": "Community Models",
        "category": "coding",
        "tasks": [
            "software development",
            "automation",
            "debugging"
        ],
        "status": "AVAILABLE"
    },

    {
        "name": "NVIDIA Accelerated Models",
        "provider": "NVIDIA NIM ecosystem",
        "category": "local_ai",
        "tasks": [
            "local inference",
            "performance workloads",
            "agent tools"
        ],
        "status": "READY_FOR_ADAPTER"
    },

    {
        "name": "Hermes Communication Model",
        "provider": "Genesis",
        "category": "communication",
        "tasks": [
            "Telegram",
            "notifications",
            "summaries"
        ],
        "status": "ONLINE"
    }

]


registry = {

    "system":
    "GENESIS MODEL REGISTRY",

    "timestamp":
    str(datetime.now()),

    "routing_policy":
    "Assign model based on agent task",

    "models":
    models

}


print(json.dumps(registry, indent=4))
