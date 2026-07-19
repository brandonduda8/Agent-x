from core.genesis.runtime.genesis_runtime import genesis_runtime


print("=" * 40)
print("🧬 GENESIS RUNTIME TEST")
print("=" * 40)


genesis_runtime.start()


print(
    genesis_runtime.cycle()
)


print(
    genesis_runtime.status()
)
