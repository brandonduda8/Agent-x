from core.genesis.telegram.telegram_daemon import (
    telegram_daemon
)


print("="*40)
print("🧬 GENESIS TELEGRAM DAEMON TEST")
print("="*40)


print(
    telegram_daemon.start()
)


print(
    telegram_daemon.listen_once()
)
