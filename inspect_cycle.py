from core.genesis.omega.command_center.genesis_autonomous_cycle_engine import (
    genesis_autonomous_cycle_engine
)

print("SYSTEM:")
print(type(genesis_autonomous_cycle_engine))

print("\nMETHODS:")
print(
    [
        x for x in dir(genesis_autonomous_cycle_engine)
        if not x.startswith("_")
    ]
)
