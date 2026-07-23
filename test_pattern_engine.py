
from genesis_core.patterns.pattern_engine import GenesisPatternEngine


engine = GenesisPatternEngine()


memories = [

{

"type":
"revenue",

"data":
{

"client":
"Dental AI",

"value":
999

}

},

{

"type":
"agent_performance",

"data":
{

"agent":
"Agent-X",

"score":
95

}

}

]


print(
engine.analyze_memory(
memories
)
)


print(
engine.recommend()
)


print(
engine.status()
)

