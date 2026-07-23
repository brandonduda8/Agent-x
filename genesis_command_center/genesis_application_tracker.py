import json
from datetime import datetime


tracker = {

    "system": "GENESIS APPLICATION TRACKER",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Track applications and improve opportunity outcomes",

    "application_fields":
    [
        "company",
        "role",
        "location",
        "resume_profile",
        "date_applied",
        "status",
        "response",
        "interview_stage",
        "outcome"
    ],

    "statuses":
    [
        "DISCOVERED",
        "REVIEWED",
        "APPROVED",
        "APPLIED",
        "INTERVIEW",
        "OFFER",
        "REJECTED",
        "FOLLOW_UP"
    ],

    "learning_metrics":
    [
        "response_rate",
        "best_resume_profile",
        "best_role_match",
        "best_company_types"
    ],

    "approval_policy":
    "Applications require operator approval",

    "memory":
    "Results stored for future opportunity scoring"

}


print(json.dumps(tracker, indent=4))
