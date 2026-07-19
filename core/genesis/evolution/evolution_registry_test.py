from core.genesis.evolution.capability_registry import (
    capability_registry
)

from core.genesis.evolution.agent_genome import (
    agent_genome
)

from core.genesis.evolution.agent_version_manager import (
    agent_version_manager
)


print("=" * 60)
print("🧬 GENESIS EVOLUTION REGISTRY TEST")
print("=" * 60)


genome = agent_genome.create_genome(
    "Lead Generation Agent",
    [
        "lead_generation",
        "research"
    ]
)


capability = capability_registry.register_capability(
    "Lead Generation Agent",
    "advanced_prospect_filtering"
)


updated = agent_version_manager.upgrade_agent(
    genome,
    capability
)


print(updated)

print(
    capability_registry.report()
)
