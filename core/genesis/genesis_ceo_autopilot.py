import time
import uuid

from core.genesis.event_stream import event_stream

from core.genesis.daily_revenue_loop import (
    daily_revenue_loop
)

from core.genesis.client_pipeline import (
    client_pipeline
)

from core.genesis.genesis_health_monitor import (
    genesis_health_monitor
)

from core.genesis.telegram_bridge import (
    telegram_bridge
)


class GenesisCEOAutopilot:

    """
    GENESIS CEO AUTOPILOT v1

    Executive decision layer.

    Responsibilities:

    - monitor Genesis health
    - review revenue pipeline
    - create revenue cycles
    - produce CEO briefings
    - notify operator
    """

    def __init__(self):

        self.system = (
            "GENESIS CEO AUTOPILOT v1"
        )

        self.cycles = []



    def run_cycle(self):

        print(
            "🧬 CEO AUTOPILOT CYCLE START"
        )


        health = (
            genesis_health_monitor
            .run_check()
        )


        leads = (
            client_pipeline
            .get_leads()
        )


        pipeline = (
            client_pipeline
            .revenue_report()
        )


        opportunities = []

        for lead in leads:

            opportunities.append(
                {
                    "title":
                    lead.get(
                        "opportunity"
                    ),

                    "skills":
                    [
                        "sales",
                        "automation",
                        "ai"
                    ],

                    "value":
                    1500
                }
            )



        profile = {

            "skills":
            [
                "sales",
                "automation",
                "ai"
            ]

        }


        revenue_cycle = (
            daily_revenue_loop
            .create_cycle(
                opportunities,
                profile
            )
        )


        briefing = {

            "id":
            "ceo_" +
            uuid.uuid4().hex[:8],

            "health":
            health["status"],

            "leads":
            len(leads),

            "pipeline":
            pipeline,

            "revenue_cycle":
            revenue_cycle,

            "timestamp":
            time.time()

        }


        self.cycles.append(
            briefing
        )


        event_stream.emit(
            "GENESIS_CEO_BRIEFING",
            self.system,
            briefing
        )


        message = (
            "🧬 GENESIS CEO BRIEFING\n\n"
            f"Health: {health['status']}\n\n"
            f"Active Leads: {len(leads)}\n\n"
            "Revenue Pipeline:\n"
            + str(pipeline)
        )


        try:

            telegram_bridge.send(
                message
            )

        except Exception:

            pass



        return briefing



    def report(self):

        return {

            "system":
            self.system,

            "cycles":
            len(self.cycles),

            "timestamp":
            time.time()

        }



genesis_ceo_autopilot = GenesisCEOAutopilot()
