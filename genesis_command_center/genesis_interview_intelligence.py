import json
from datetime import datetime


engine = {

    "system": "GENESIS INTERVIEW INTELLIGENCE ENGINE",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Prepare operator for successful interviews",

    "inputs":
    [
        "Opportunity Vault",
        "Profile Vault",
        "Resume Intelligence"
    ],

    "analysis":
    [
        "Company research",
        "Role requirements",
        "Skill alignment",
        "Potential questions",
        "Answer preparation"
    ],

    "outputs":
    [
        "Interview briefing",
        "Custom talking points",
        "STAR examples",
        "Questions to ask employer",
        "Follow-up message draft"
    ],

    "answer_framework":
    {
        "method":
        "STAR",

        "components":
        [
            "Situation",
            "Task",
            "Action",
            "Result"
        ]
    },

    "approval_policy":
    {
        "interview_messages":
        "REQUIRED",

        "external_contact":
        "REQUIRED"
    },

    "memory":
    "Store interview outcomes to improve future preparation"

}


print(json.dumps(engine, indent=4))
