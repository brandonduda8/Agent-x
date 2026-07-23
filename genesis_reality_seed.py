from core.genesis.genesis_reality_connectors import reality_connectors
from core.genesis.genesis_result_harvester import result_harvester


# Income targets
jobs = [
    "Local employers hiring immediately",
    "Remote customer support roles",
    "AI automation assistant contracts",
    "Technical support positions"
]


# Revenue targets
leads = [
    "Dental clinics needing AI receptionist automation",
    "Small businesses needing workflow automation",
    "Companies needing AI process improvement"
]


# Stability targets
housing = [
    "Local housing assistance programs",
    "Emergency housing resources",
    "Rental support programs"
]


for item in jobs:
    reality_connectors.collect_job(item)
    result_harvester.record(
        "income",
        item,
        "Opportunity Discovery Agent"
    )


for item in leads:
    reality_connectors.collect_business_lead(item)
    result_harvester.record(
        "revenue",
        item,
        "Revenue Agent"
    )


for item in housing:
    reality_connectors.collect_housing_resource(item)
    result_harvester.record(
        "housing",
        item,
        "Stability Agent"
    )


print(reality_connectors.status())
print(result_harvester.status())
