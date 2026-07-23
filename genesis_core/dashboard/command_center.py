import time


class GenesisUnifiedCommandCenter:


    def __init__(
        self,
        systems=None
    ):

        self.systems = systems or {}



    def register(
        self,
        name,
        system
    ):

        self.systems[name] = system



    def status(self):

        report = {


            "system":
            "GENESIS UNIFIED COMMAND CENTER v1",


            "status":
            "ONLINE",


            "timestamp":
            time.time(),


            "modules": {}

        }


        for name, system in self.systems.items():


            try:

                if hasattr(system, "status"):

                    report["modules"][name] = (
                        system.status()
                    )


                elif hasattr(system, "report"):

                    report["modules"][name] = (
                        system.report()
                    )


                else:

                    report["modules"][name] = {
                        "status":
                        "CONNECTED"
                    }


            except Exception as error:


                report["modules"][name] = {

                    "status":
                    "ERROR",

                    "error":
                    str(error)

                }


        return report



    def executive_brief(
        self,
        priorities
    ):


        return {


            "system":
            "GENESIS EXECUTIVE BRIEF",


            "mission":
            "Create economic stability and build wealth",


            "top_priorities":
            priorities,


            "timestamp":
            time.time()

        }
