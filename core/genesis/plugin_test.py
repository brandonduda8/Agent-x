from core.genesis.plugin_manager import plugin_manager


print(
    plugin_manager.load(
        "telegram",
        "core.genesis.telegram_bridge",
        "telegram_bridge"
    )
)


print(
    plugin_manager.report()
)
