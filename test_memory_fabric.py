
from genesis_core.memory.memory_fabric import GenesisMemoryFabric


memory = GenesisMemoryFabric()


print(
memory.store(

"revenue",

"Genesis Economic OS",

{

"client":
"Dental AI Reception Automation",

"value":
999

}

)
)


print(
memory.store(

"agent_performance",

"Performance Engine",

{

"agent":
"Agent-X",

"score":
95

}

)
)


print(
memory.store(

"mission",

"CEO Loop",

{

"objective":
"Acquire Dental AI Client"

}

)
)


print(
memory.search(
"revenue"
)
)


print(
memory.summarize()
)

