import json
from datetime import datetime


scanner = {

    "system": "GENESIS OPPORTUNITY SCANNER",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Discover and organize high probability income opportunities",

    "sources":
    [
        {
            "name": "Remote Job Sources",
            "categories":
            [
                "Technical Support",
                "Help Desk",
                "Customer Support",
                "AI Assistant"
            ]
        },

        {
            "name": "Company Career Pages",
            "categories":
            [
                "Entry Technology Roles",
                "Support Engineering",
                "Operations"
            ]
        },

        {
            "name": "Learning Path Opportunities",
            "categories":
            [
                "Certifications",
                "Portfolio Projects",
                "Career Transition"
            ]
        }
    ],

    "workflow":
    [
        "Collect opportunity",
        "Score compatibility",
        "Match resume profile",
        "Store in Opportunity Vault",
        "Request operator approval"
    ],

    "approval":
    {
        "applications": "REQUIRED",
        "external_contact": "REQUIRED"
    }

}


print(json.dumps(scanner, indent=4))
