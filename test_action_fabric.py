
from genesis_core.actions.action_fabric import GenesisActionFabric


fabric = GenesisActionFabric()


action = fabric.create_action(

"business",

"Acquire Dental AI Client",

{

"offer":
"AI Reception Automation",

"value":
999

}

)


print(action)


approved = fabric.approve_action(
action["id"]
)


print(approved)


result = fabric.record_result(

action["id"],

"Outreach campaign prepared",

True

)


print(result)


print(
fabric.status()
)

