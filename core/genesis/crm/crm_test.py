from core.genesis.crm.contact_manager import (
    contact_manager
)

from core.genesis.crm.opportunity_tracker import (
    opportunity_tracker
)

from core.genesis.crm.conversation_memory import (
    conversation_memory
)

from core.genesis.crm.pipeline_manager import (
    pipeline_manager
)


print("=" * 60)
print("🧠 GENESIS CRM RELATIONSHIP ENGINE TEST")
print("=" * 60)


contact = contact_manager.create_contact(
    "Healthcare AI Prospect",
    "Healthcare AI",
    "CEO"
)


contact["pain_points"] = [
    "manual workflows",
    "missed opportunities"
]

contact["score"] = 92


opportunity = opportunity_tracker.create_opportunity(
    contact,
    "AI Automation Implementation Package"
)


pipeline_manager.move_stage(
    opportunity,
    "CONTACTED"
)


conversation = conversation_memory.store(
    contact["company"],
    "Interested in automation savings",
    "FOLLOW_UP_REQUIRED"
)


print({
    "contact": contact,
    "opportunity": opportunity,
    "conversation": conversation
})


print({
    "system": "GENESIS CRM RELATIONSHIP ENGINE v1",
    "contacts": len(contact_manager.contacts),
    "opportunities": len(opportunity_tracker.opportunities),
    "conversations": len(conversation_memory.conversations)
})
