
from genesis_core.workforce.workforce_engine import GenesisWorkforceEngine


workforce = GenesisWorkforceEngine()


ceo = workforce.register_agent(

"Genesis CEO Agent",

"strategy",

[

"planning",

"reasoning"

]

)


coder = workforce.register_agent(

"Agent-X Coding Agent",

"engineering",

[

"coding",

"deployment"

]

)


workforce.update_performance(

coder["id"],

95

)


print(ceo)

print(coder)


print(

workforce.find_agent(

"coding"

)

)


print(

workforce.create_agent_design(

"marketing"

)

)


print(

workforce.status()

)

