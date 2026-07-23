import json
from datetime import datetime


adapter = {

    "system": "GENESIS JOB SOURCE ADAPTER",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Collect and normalize career opportunities",

    "sources":
    [
        {
            "name": "Remote Job Boards",
            "categories":
            [
                "Technical Support",
                "Help Desk",
                "Customer Success",
                "AI Assistant"
            ]
        },

        {
            "name": "Company Career Pages",
            "categories":
            [
                "Entry IT",
                "Operations",
                "Support Engineering"
            ]
        },

        {
            "name": "Learning Path Sources",
            "categories":
            [
                "Certifications",
                "Portfolio Projects"
            ]
        }
    ],

    "processing":
    [
        "Collect opportunity",
        "Normalize data",
        "Score compatibility",
        "Match resume profile",
        "Store in Opportunity Vault"
    ],

    "approval":
    {
        "applications":
        "REQUIRED",

        "external_contact":
        "REQUIRED"
    }

}


print(json.dumps(adapter, indent=4))
