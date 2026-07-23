import time


class GenesisTelegramSalesCenter:

    """
    GENESIS TELEGRAM SALES CENTER v1

    Revenue control interface.
    """

    def __init__(
        self,
        client_pipeline=None,
        acquisition_loop=None,
        revenue_autopilot=None
    ):

        self.system = (
            "GENESIS TELEGRAM SALES CENTER v1"
        )

        self.client_pipeline = client_pipeline
        self.acquisition_loop = acquisition_loop
        self.revenue_autopilot = revenue_autopilot



    def process(
        self,
        command
    ):

        text = command.lower().strip()


        if text == "/status":

            return (
                "🧬 GENESIS ONLINE\n\n"
                "Revenue Engine: ACTIVE\n"
                "Lead System: ACTIVE\n"
                "Telegram Control: ACTIVE"
            )



        if text == "/leads":

            if not self.client_pipeline:

                return "No pipeline connected."


            leads = (
                self.client_pipeline
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


            return response



        if text == "/high_priority":

            if not self.acquisition_loop:

                return "Acquisition system offline."


            results = (
                self.acquisition_loop
                .run_cycle()
            )


            response = (
                "🔥 HIGH PRIORITY LEADS\n\n"
            )


            for item in results:

                if (
                    item["lead"]["priority"]
                    == "HIGH"
                ):

                    response += (
                        f"{item['lead']['company']}\n"
                        f"Score: {item['lead']['score']}\n\n"
                    )


            return response



        if text == "/run_cycle":

            if not self.revenue_autopilot:

                return "Revenue autopilot offline."


            results = (
                self.revenue_autopilot
                .run_pipeline()
            )


            return (
                "🚀 Revenue cycle complete\n"
                f"Created campaigns: {len(results)}"
            )



        return (
            "Genesis received command.\n"
            "Available:\n\n"
            "/status\n"
            "/leads\n"
            "/high_priority\n"
            "/run_cycle"
        )



    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
