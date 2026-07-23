import time


class GenesisCommandRouter:


    def __init__(
        self,
        systems
    ):

        self.systems = systems



    def route(
        self,
        command
    ):

        command = command.strip().lower()


        if command == "/status":

            return self.status()


        if command == "/opportunities":

            return self.opportunities()


        if command == "/missions":

            return self.missions()


        if command == "/today":

            return self.today()


        if command == "/help":

            return self.help()


        return {

            "message":
            "Unknown command. Use /help"

        }



    def status(self):

        return {

            "system":
            "GENESIS OS",

            "status":
            "ONLINE",

            "systems":
            self.systems.get(
                "systems",
                []
            ),

            "timestamp":
            time.time()

        }



    def opportunities(self):

        return {

            "top_opportunities":
            self.systems.get(
                "opportunities",
                []
            )

        }



    def missions(self):

        return {

            "active_missions":
            self.systems.get(
                "missions",
                []
            )

        }



    def today(self):

        return {

            "daily_plan":

            [

                "Review highest-value opportunity",

                "Complete income-generating action",

                "Advance client pipeline",

                "Improve Genesis system"

            ]

        }



    def help(self):

        return {

            "commands":

            [

                "/status",

                "/opportunities",

                "/missions",

                "/today",

                "/help"

            ]

        }
