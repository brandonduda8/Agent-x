import time

from core.genesis.genesis_bootstrap import (
    genesis_command_center
)

from core.genesis.genesis_workforce_controller import (
    genesis_workforce_controller
)

from core.genesis.client_pipeline import (
    client_pipeline
)

from core.genesis.client_acquisition_loop import (
    client_acquisition_loop
)


class GenesisTelegramCommandCenter:

    """
    GENESIS TELEGRAM COMMAND CENTER v2

    Unified Telegram interface.

    Controls:
    - Genesis missions
    - Workforce
    - Revenue pipeline
    - Lead intelligence
    """

    def __init__(self):

        self.system = (
            "GENESIS TELEGRAM COMMAND CENTER v2"
        )

        self.commands = []



    def process(
        self,
        message
    ):

        text = message.strip()

        lower = text.lower()

        result = {

            "command":
                text,

            "timestamp":
                time.time()

        }



        if lower.startswith("/status"):

            result["response"] = (
                "🧬 GENESIS ONLINE\n\n"
                + str(
                    genesis_command_center
                    .generate_report()
                )
            )



        elif lower.startswith("/mission"):

            objective = (
                text.replace(
                    "/mission",
                    "",
                    1
                )
                .strip()
            )

            if not objective:

                objective = (
                    "Create revenue opportunity"
                )


            mission = (
                genesis_command_center
                .submit_goal(
                    objective
                )
            )


            result["response"] = (
                "🧬 Mission Created\n\n"
                + str(mission)
            )



        elif lower.startswith("/agents"):

            result["response"] = str(
                genesis_workforce_controller
                .report()
            )



        elif lower.startswith("/leads"):

            leads = (
                client_pipeline
                .get_leads()
            )


            response = (
                "🧬 GENESIS LEADS\n\n"
            )


            for lead in leads:

                response += (
                    f"{lead['company']}\n"
                    f"Problem: {lead['problem']}\n"
                    f"Opportunity: {lead['opportunity']}\n\n"
                )


            result["response"] = response



        elif lower.startswith("/high_priority"):

            results = (
                client_acquisition_loop
                .run_cycle()
            )


            response = (
                "🔥 HIGH PRIORITY LEADS\n\n"
            )


            for item in results:

                lead = item["lead"]

                if (
                    lead["priority"]
                    == "HIGH"
                ):

                    response += (
                        f"{lead['company']}\n"
                        f"Score: {lead['score']}\n\n"
                    )


            result["response"] = response



        elif lower.startswith("/revenue"):

            result["response"] = (
                "💰 GENESIS REVENUE SYSTEM\n\n"
                + str(
                    client_pipeline
                    .revenue_report()
                )
            )



        elif lower.startswith("/report"):

            result["response"] = str(
                genesis_command_center
                .generate_report()
            )



        elif lower.startswith("/help"):

            result["response"] = (

                "🧬 Genesis Commands\n\n"

                "/status\n"
                "/mission <goal>\n"
                "/agents\n"
                "/leads\n"
                "/high_priority\n"
                "/revenue\n"
                "/report\n"
                "/help"

            )



        else:

            mission = (
                genesis_command_center
                .submit_goal(
                    text
                )
            )

            result["response"] = (
                "🧬 Genesis Mission Created\n\n"
                + str(mission)
            )



        self.commands.append(
            result
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "commands":
                len(self.commands),

            "timestamp":
                time.time()

        }



telegram_command_center = GenesisTelegramCommandCenter()
