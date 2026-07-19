import time

from core.genesis.runtime.genesis_runtime import genesis_runtime
from core.genesis.ceo.ceo_loop_runner import ceo_loop_runner

try:
    from core.genesis.telegram.telegram_daemon import telegram_daemon
    TELEGRAM_AVAILABLE = True
except Exception as e:
    TELEGRAM_AVAILABLE = False
    TELEGRAM_ERROR = str(e)


class GenesisStart:

    def __init__(self):
        self.system = "GENESIS AUTONOMOUS BUSINESS OS v1"
        self.started = time.time()

    def boot(self):

        print("=" * 50)
        print("🧬 GENESIS AUTONOMOUS BUSINESS OS")
        print("=" * 50)

        print("🚀 Starting Runtime...")
        genesis_runtime.start()

        print("👑 Starting CEO Loop...")
        ceo_loop_runner.run_cycle(
            "Launch autonomous revenue operation"
        )

        if TELEGRAM_AVAILABLE:
            print("📲 Starting Telegram Daemon...")
            telegram_daemon.start()
        else:
            print("⚠️ Telegram unavailable:")
            print(TELEGRAM_ERROR)

        print()
        print("✅ Genesis Online")
        print()

        return self.status()

    def status(self):

        return {
            "system": self.system,
            "runtime": genesis_runtime.status(),
            "ceo": ceo_loop_runner.report(),
            "telegram": TELEGRAM_AVAILABLE,
            "started": self.started
        }


genesis = GenesisStart()


if __name__ == "__main__":
    print(genesis.boot())
