import time


class GenesisTelegramController:

    """
    GENESIS TELEGRAM CONTROLLER v1

    Human interface layer.

    Connects:
    Telegram
        |
    Genesis Command Center
        |
    Workforce
        |
    Memory
    """


    def __init__(
        self,
        command_center=None,
        heartbeat=None,
        memory=None,
        telegram_bridge=None
    ):

        self.system = "GENESIS TELEGRAM CONTROLLER v1"

        self.command_center = command_center
        self.heartbeat = heartbeat
        self.memory = memory
        self.telegram_bridge = telegram_bridge



    def process(self, text):

        text = text.strip()


        if text.startswith("/status"):

            return self.status()



        if text.startswith("/mission"):

            goal = text.replace(
                "/mission",
                ""
            ).strip()

            return self.create_mission(goal)



        if text.startswith("/report"):

            return self.report()



        if text.startswith("/agents"):

            return self.agents()



        if text.startswith("/learn"):

            return self.learn()



        return {
            "response":
            "Unknown Genesis command."
        }



    def create_mission(self, goal):

        if not self.command_center:

            return {
                "response":
                "Genesis Command Center unavailable"
            }


        mission = self.command_center.submit_goal(
            goal
        )


        return {
            "response":
            f"""
🧬 GENESIS MISSION CREATED

ID:
{mission['id']}

Objective:
{mission['objective']}

Agents:
{mission.get('agents', [])}

Status:
{mission['status']}
"""
        }



    def status(self):

        report = {}

        if self.command_center:
            report["command_center"] = (
                self.command_center.generate_report()
            )


        if self.heartbeat:
            report["heartbeat"] = (
                self.heartbeat.workforce_status()
            )


        return {
            "response":
            str(report)
        }



    def report(self):

        return self.status()



    def agents(self):

        if self.heartbeat:

            return {
                "response":
                str(
                    self.heartbeat.workforce_status()
                )
            }


        return {
            "response":
            "No heartbeat system connected"
        }



    def learn(self):

        if self.memory:

            return {
                "response":
                str(
                    self.memory.report()
                )
            }


        return {
            "response":
            "Memory unavailable"
        }



genesis_telegram_controller = GenesisTelegramController()
