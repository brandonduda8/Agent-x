print("="*60)
print("🏢 GENESIS COMPANY OPERATOR TEST")
print("="*60)


from core.genesis.company.company_operator import (
    company_operator
)


result = company_operator.create_company(
    "Healthcare AI Automation Company",
    "Healthcare AI",
    "Acquire first AI automation customers"
)


print(result)

print(
    company_operator.report()
)
