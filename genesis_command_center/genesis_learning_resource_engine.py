import json
from datetime import datetime


engine = {

    "system": "GENESIS LEARNING RESOURCE INTELLIGENCE ENGINE",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "mission":
    "Find highest-value free learning resources for career transition",

    "learning_targets":
    [
        {
            "skill": "IT Support Fundamentals",
            "goal": "Qualify for help desk roles"
        },
        {
            "skill": "Networking Basics",
            "goal": "Improve technical troubleshooting ability"
        },
        {
            "skill": "Python Automation",
            "goal": "Build automation portfolio"
        },
        {
            "skill": "AI Workflow Tools",
            "goal": "Prepare for AI operations roles"
        }
    ],

    "resource_categories":
    [
        "Free courses",
        "Open source projects",
        "Practice labs",
        "Documentation",
        "Portfolio projects"
    ],

    "priority_order":
    [
        "Income impact",
        "Career relevance",
        "Time efficiency",
        "Free availability"
    ],

    "outputs":
    [
        "Learning roadmap",
        "Recommended resources",
        "Portfolio projects",
        "Skill completion tracking"
    ],

    "memory":
    "Track completed learning and improve recommendations"

}


print(json.dumps(engine, indent=4))
