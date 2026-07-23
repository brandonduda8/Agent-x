import json
from datetime import datetime


engine = {

    "system": "GENESIS SKILL GROWTH ENGINE",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Identify highest-value skills for career transition",

    "inputs":
    [
        "Profile Vault",
        "Career Targets",
        "Opportunity Intelligence"
    ],

    "current_strengths":
    [
        "Communication",
        "Customer relations",
        "Problem solving",
        "Reliability",
        "Working under pressure"
    ],

    "recommended_growth":
    [
        {
            "skill": "IT Support Fundamentals",
            "reason": "Highest match for technical support transition"
        },
        {
            "skill": "Python Automation",
            "reason": "Supports AI and automation pathway"
        },
        {
            "skill": "Networking Basics",
            "reason": "Improves help desk eligibility"
        },
        {
            "skill": "AI Workflow Tools",
            "reason": "Supports automation assistant roles"
        }
    ],

    "learning_policy":
    "Prioritize free or low-cost resources",

    "memory":
    "Track completed skills and career outcomes"

}


print(json.dumps(engine, indent=4))
