import json
from datetime import datetime


agent_requests = [

    {
        "agent": "Genesis Executive",
        "task": "Create daily strategy",
        "category": "reasoning"
    },

    {
        "agent": "Revenue Agent",
        "task": "Prepare business outreach",
        "category": "reasoning"
    },

    {
        "agent": "Technology Agent",
        "task": "Build automation tools",
        "category": "coding"
    },

    {
        "agent": "Hermes Agent",
        "task": "Send Telegram briefing",
        "category": "communication"
    }

]


routing = {

    "reasoning":
    "OpenAI Reasoning Model",

    "coding":
    "Open Source Code Models",

    "local_ai":
    "NVIDIA Accelerated Models",

    "communication":
    "Hermes Communication Model"

}


results = []


for request in agent_requests:

    results.append({

        "agent":
        request["agent"],

        "task":
        request["task"],

        "selected_model":
        routing.get(
            request["category"],
            "No model assigned"
        ),

        "status":
        "ROUTED"

    })


output = {

    "system":
    "GENESIS MODEL ROUTER",

    "timestamp":
    str(datetime.now()),

    "policy":
    "Select best available model by capability",

    "routes":
    results

}


print(json.dumps(output, indent=4))
