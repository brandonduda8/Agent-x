import json
from datetime import datetime


agents = [

    {
        "agent": "Genesis Executive",

        "role": "Strategic coordination",

        "model":
        "OpenAI Reasoning Model",

        "adapters": [
            "Event Bus",
            "Memory Engine",
            "Decision Bridge"
        ],

        "capabilities": [
            "Analyze missions",
            "Rank priorities",
            "Create executive briefs"
        ],

        "permissions": {
            "analysis": "ALLOWED",
            "external_actions": "APPROVAL_REQUIRED"
        }
    },


    {
        "agent": "Revenue Agent",

        "role": "Business development",

        "model":
        "OpenAI Reasoning Model",

        "adapters": [
            "CRM Adapter",
            "Telegram Adapter",
            "Business Lead Adapter"
        ],

        "capabilities": [
            "Find leads",
            "Score opportunities",
            "Draft outreach"
        ],

        "permissions": {
            "draft_messages": "ALLOWED",
            "contact_clients": "APPROVAL_REQUIRED"
        }
    },


    {
        "agent": "Opportunity Discovery Agent",

        "role": "Income discovery",

        "model":
        "OpenAI Reasoning Model",

        "adapters": [
            "Job Discovery Adapter",
            "Opportunity Vault"
        ],

        "capabilities": [
            "Find opportunities",
            "Rank jobs",
            "Track applications"
        ],

        "permissions": {
            "analysis": "ALLOWED",
            "applications": "APPROVAL_REQUIRED"
        }
    },


    {
        "agent": "Technology Agent",

        "role":
        "Automation engineering",

        "model":
        "Open Source Code Models",

        "adapters": [
            "Agent Harness",
            "OpenClaw Bridge"
        ],

        "capabilities": [
            "Build tools",
            "Improve adapters",
            "Debug systems"
        ],

        "permissions": {
            "code_changes":
            "APPROVAL_REQUIRED"
        }
    },


    {
        "agent": "Hermes Agent",

        "role":
        "Communication intelligence",

        "model":
        "Hermes Communication Model",

        "adapters": [
            "Telegram Adapter",
            "Phone Adapter"
        ],

        "capabilities": [
            "Send briefings",
            "Format notifications",
            "Route approvals"
        ],

        "permissions": {
            "notifications":
            "ALLOWED",

            "external_messages":
            "APPROVAL_REQUIRED"
        }
    }

]


output = {

    "system":
    "GENESIS AGENT CAPABILITY MATRIX",

    "timestamp":
    str(datetime.now()),

    "policy":
    "Every agent operates within assigned permissions",

    "agents":
    agents

}


print(json.dumps(output, indent=4))
