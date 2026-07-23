
from genesis_core.world.world_connector import GenesisWorldConnector


world = GenesisWorldConnector()


jobs = world.register_source(

"Remote Job Intelligence",

"employment"

)


business = world.register_source(

"Business Intelligence",

"business"

)


print(
world.ingest(

jobs,

"AI Automation Assistant",

"Remote AI workflow support",

1000

)
)


print(
world.ingest(

business,

"Dental AI Reception Automation",

"Missed calls and lost appointments",

999

)
)


print(
world.scan()
)

