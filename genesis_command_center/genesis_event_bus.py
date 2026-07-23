import json
from datetime import datetime


events = []


def emit(agent, event_type, message, approval_required=False):

    event = {
        "id": len(events) + 1,
        "agent": agent,
        "type": event_type,
        "message": message,
        "approval_required": approval_required,
        "timestamp": str(datetime.now()),
        "status": "WAITING_APPROVAL" if approval_required else "READY"
    }

    events.append(event)
    return event



system = {
    "system": "GENESIS EVENT BUS",

    "timestamp": str(datetime.now()),

    "status": "ONLINE",

    "routing": {
        "income_events": "Opportunity Discovery Agent",
        "business_events": "Revenue Agent",
        "communication_events": "Hermes Agent",
        "system_events": "Technology Agent"
    },

    "test_events": [
        emit(
            "Revenue Agent",
            "BUSINESS_OPPORTUNITY",
            "Potential client outreach prepared",
            True
        ),

        emit(
            "Opportunity Discovery Agent",
            "INCOME_OPPORTUNITY",
            "High probability opportunity identified",
            True
        ),

        emit(
            "Technology Agent",
            "SYSTEM_UPDATE",
            "Adapter improvement available",
            False
        )
    ]
}


print(json.dumps(system, indent=4))
