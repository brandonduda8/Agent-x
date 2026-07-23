
from genesis_core.optimizer.mission_optimizer import GenesisMissionOptimizer


optimizer = GenesisMissionOptimizer()


mission = optimizer.create_mission({

"name":
"Dental AI Reception Automation",

"value":
999,

"urgency":
90,

"automation_fit":
95,

"speed":
85

})


print(mission)


print(
optimizer.best_mission()
)


print(
optimizer.status()
)

