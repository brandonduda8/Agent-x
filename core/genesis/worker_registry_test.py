from core.genesis.worker_registry import worker_registry


worker_registry.register_worker(
    "Offer Builder",
    "Creates revenue offers and packages",
    [
        "pricing",
        "proposals",
        "service design"
    ]
)


worker_registry.register_worker(
    "Lead Hunter",
    "Finds potential customers",
    [
        "research",
        "lead generation",
        "market analysis"
    ]
)


worker_registry.register_worker(
    "Content Agent",
    "Creates marketing assets",
    [
        "copywriting",
        "video ideas",
        "social posts"
    ]
)


worker_registry.register_worker(
    "Sales Agent",
    "Handles sales workflow",
    [
        "outreach",
        "follow ups",
        "customer conversations"
    ]
)


worker_registry.register_worker(
    "Research Agent",
    "Finds opportunities and intelligence",
    [
        "web research",
        "trend analysis",
        "competition"
    ]
)


print(
    worker_registry.report()
)
