import time


class GenesisTelegramGateway:

    """
    GENESIS TELEGRAM GATEWAY v1

    Human communication layer.

    Telegram
        |
    Genesis Command Center
        |
    Mission System
        |
    Workforce
        |
    Memory
    """

    def __init__(
        self,
        command_center=None,
        command_router=None,
        telegram_bridge=None
    ):

        self.system = "GENESIS TELEGRAM GATEWAY v1"

        self.command_center = command_center
        self.command_router = command_router
        self.telegram_bridge = telegram_bridge

        self.messages = []


    def handle(self, message):

        print(
            "📲 Genesis Telegram:",
            message
        )


        # Mission command

        if message.startswith("/mission"):

            goal = message.replace(
                "/mission",
                ""
            ).strip()


            if self.command_center:

                mission = (
                    self.command_center
                    .submit_goal(goal)
                )


                response = f"""
🧬 GENESIS MISSION CREATED

ID:
{mission['id']}

OBJECTIVE:
{mission['objective']}

AGENTS:
{mission.get('agents', [])}

STATUS:
{mission['status']}
"""


                self.send(response)

                return response



        # Status command

        if message.startswith("/status"):

            if self.command_center:

                response = str(
                    self.command_center
                    .generate_report()
                )

                self.send(response)

                return response



        # Existing Genesis commands

        if self.command_router:

            result = (
                self.command_router
                .process(message)
            )

            self.send(
                result["response"]
            )

            return result["response"]


        return "Genesis gateway online"



    def send(self, message):

        self.messages.append(
            {
                "message": message,
                "timestamp": time.time()
            }
        )


        if self.telegram_bridge:

            try:
                self.telegram_bridge.send(
                    message
                )

            except Exception:
                pass



        return {
            "status": "QUEUED"
        }



    def report(self):

        return {
            "system": self.system,
            "messages": len(self.messages),
            "timestamp": time.time()
        }



genesis_telegram_gateway = GenesisTelegramGateway()
