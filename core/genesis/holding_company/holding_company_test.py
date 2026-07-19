from core.genesis.holding_company.holding_company import (
    holding_company
)


print("="*60)
print("👑 GENESIS HOLDING COMPANY TEST")
print("="*60)


company = {

    "name":
    "Healthcare AI Automation Company",

    "market":
    "Healthcare AI"

}


result = holding_company.operate(
    company
)


print(result)


print({

"system":
holding_company.system,

"cycles":
len(holding_company.cycles)

})
