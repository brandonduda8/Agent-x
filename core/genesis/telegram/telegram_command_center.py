import time

from core.genesis.runtime.genesis_runtime import genesis_runtime


class GenesisTelegramCommandCenter:

    def __init__(self):
        self.system = "GENESIS TELEGRAM COMMAND CENTER v1"


    def process(self, command):

        cmd = command.lower().strip()


        if cmd == "/status":

            return self.status()


        if cmd == "/runtime":

            return str(
                genesis_runtime.status()
            )


        if cmd == "/cycle":

            return str(
                genesis_runtime.cycle()
            )


        if cmd == "/help":

            return (
                "Genesis Commands:\n"
                "/status\n"
                "/runtime\n"
                "/cycle\n"
                "/help"
            )


        return (
            "Genesis received:\n"
            + command
        )


    def status(self):

        state = genesis_runtime.status()

        return (
            "🧬 GENESIS STATUS\n\n"
            f"Runtime: {state['running']}\n"
            f"Cycles: {state['cycles']}\n"
            "System: ONLINE"
        )


telegram_command_center = GenesisTelegramCommandCenter()
