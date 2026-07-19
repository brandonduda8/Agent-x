print("="*60)
print("⚡ GENESIS SWARM INTELLIGENCE TEST")
print("="*60)


from core.genesis.swarm.swarm_commander import (
    swarm_commander
)


result = swarm_commander.create_swarm(
    "Acquire AI automation customers with sales"
)


print(result)

print(
    swarm_commander.report()
)
