from core.genesis.device_capability_manager import device_capability_manager


print(
    device_capability_manager.discover_device_stack()
)


print(
    device_capability_manager.report()
)
