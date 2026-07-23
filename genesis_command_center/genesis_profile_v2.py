import json
from datetime import datetime


profile = {

    "system": "GENESIS OPERATOR PROFILE VAULT V2",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "operator":
    {
        "name": "Brandon Duda",
        "email": "brandonduda8@gmail.com",
        "phone": "+1 (630) 210-5724",
        "location": "Lisle, Illinois"
    },

    "mission":
    [
        "Secure immediate income",
        "Build long-term career stability",
        "Transition into technology",
        "Create financial independence"
    ],

    "experience":
    [
        "Customer service",
        "Restaurant operations",
        "Team collaboration",
        "Hard labor",
        "Problem solving",
        "Working under pressure"
    ],

    "skills":
    [
        "Communication",
        "Customer relations",
        "Reliability",
        "Adaptability",
        "Technology learning"
    ],

    "career_targets":
    [
        "Technical Support",
        "Help Desk",
        "Remote Customer Support",
        "AI Operations Assistant",
        "Automation Support",
        "Junior Software Pathway"
    ],

    "work_preferences":
    [
        "Remote",
        "Hybrid",
        "Relocation",
        "Flexible schedule"
    ],

    "priority_weights":
    {
        "income_stability": 40,
        "growth_potential": 25,
        "remote_fit": 20,
        "learning_value": 15
    },

    "approval_policy":
    "External actions require operator approval"

}


print(json.dumps(profile, indent=4))
