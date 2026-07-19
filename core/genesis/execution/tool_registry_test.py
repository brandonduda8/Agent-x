from core.genesis.execution.tool_registry import (
    tool_registry
)


print("=" * 60)
print("🛠️ GENESIS TOOL REGISTRY TEST")
print("=" * 60)


research = tool_registry.execute(
    "research",
    "Healthcare AI"
)


print(research)


leads = tool_registry.execute(
    "lead_generation",
    "Healthcare AI"
)


print(leads)


outreach = tool_registry.execute(
    "outreach",
    leads["leads"],
    "AI Automation Package"
)


print(outreach)


analytics = tool_registry.execute(
    "analytics",
    outreach
)


print(analytics)


print(tool_registry.report())
