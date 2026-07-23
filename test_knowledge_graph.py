
from genesis_core.knowledge.knowledge_graph import GenesisKnowledgeGraph


graph = GenesisKnowledgeGraph()


opportunity = graph.add_node(

"opportunity",

"Dental AI Reception Automation",

{

"value":
999

}

)


mission = graph.add_node(

"mission",

"Acquire Dental AI Client"

)


agent = graph.add_node(

"agent",

"Agent-X Coding Agent"

)


revenue = graph.add_node(

"revenue",

"AI Automation Client",

{

"amount":
999

}

)


print(
graph.connect(

opportunity,

"created",

mission

)
)


print(
graph.connect(

mission,

"assigned_to",

agent

)
)


print(
graph.connect(

agent,

"generated",

revenue

)
)


print(
graph.find_connections(
mission["id"]
)
)


print(
graph.status()
)

