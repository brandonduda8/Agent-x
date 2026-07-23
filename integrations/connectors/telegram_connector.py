from integrations.genesis.connector import GenesisConnector
from integrations.telegram.command_router import GenesisCommandRouter


class TelegramConnector(GenesisConnector):


    name = "Telegram Connector"


    def __init__(self):

        super().__init__()

        self.router = GenesisCommandRouter()

        self.capabilities = [
            "notifications",
            "commands",
            "alerts"
        ]


    def receive_command(self, command):

        return self.router.route(command)


    def send_message(self, message):

        return {

            "connector":
            self.name,

            "message":
            message,

            "status":
            "READY_FOR_DELIVERY"
        }
