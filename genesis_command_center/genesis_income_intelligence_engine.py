import json
from datetime import datetime


income_intelligence = {

    "system":
    "GENESIS INCOME INTELLIGENCE ENGINE",

    "timestamp":
    str(datetime.now()),

    "status":
    "ONLINE",

    "mission":
    "Optimize employment opportunity selection",

    "scoring_factors":
    {
        "skill_match": 30,
        "income_potential": 25,
        "remote_compatibility": 20,
        "growth_opportunity": 15,
        "application_probability": 10
    },

    "candidate_profile":
    {
        "experience":
        [
            "customer service",
            "restaurant operations",
            "team collaboration",
            "problem solving",
            "hard labor",
            "working under pressure"
        ],

        "transition_targets":
        [
            "technical support",
            "help desk",
            "AI support roles",
            "automation assistant",
            "junior software pathway"
        ]
    },

    "pipeline":
    [
        "Discovered",
        "Scored",
        "Resume Prepared",
        "Approval Requested",
        "Applied",
        "Interview",
        "Outcome Recorded"
    ],

    "learning":
    {
        "track_response_rate": True,
        "improve_matching": True,
        "store_results": True
    },

    "approval":
    "Operator approval required before applications"

}


print(json.dumps(income_intelligence, indent=4))
