import json
from datetime import datetime


def analyze_state():

    try:
        with open("memory.json", "r") as f:
            state = json.load(f)
    except:
        state = {}


    decisions = []


    # Income priority
    decisions.append({
        "priority": 1,
        "category": "income",
        "recommendation": "Prioritize high probability job applications",
        "reason": "Income stability is critical",
        "approval_required": True,
        "confidence": 0.90
    })


    # Revenue priority
    decisions.append({
        "priority": 2,
        "category": "revenue",
        "recommendation": "Review top business leads and prepare outreach",
        "reason": "Revenue pipeline already contains opportunities",
        "approval_required": True,
        "confidence": 0.85
    })


    # Technology priority
    decisions.append({
        "priority": 3,
        "category": "technology",
        "recommendation": "Improve automation adapters",
        "reason": "System foundation is operational",
        "approval_required": False,
        "confidence": 0.80
    })


    return {
        "system": "GENESIS DECISION INTELLIGENCE",
        "timestamp": str(datetime.now()),
        "recommendations": decisions
    }



if __name__ == "__main__":

    print(
        json.dumps(
            analyze_state(),
            indent=4
        )
    )
