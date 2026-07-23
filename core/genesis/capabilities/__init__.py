from .capability_registry import capability_registry

from .market_research import market_research
from .lead_generation import lead_generation
from .offer_creation import offer_creation
from .outreach import outreach
from .sales_pipeline import sales_pipeline
from .workflow_automation import workflow_automation


def register_all_capabilities():

    capability_registry.register(
        "market_research",
        market_research
    )

    capability_registry.register(
        "lead_generation",
        lead_generation
    )

    capability_registry.register(
        "offer_creation",
        offer_creation
    )

    capability_registry.register(
        "outreach",
        outreach
    )

    capability_registry.register(
        "sales_pipeline",
        sales_pipeline
    )

    capability_registry.register(
        "workflow_automation",
        workflow_automation
    )
