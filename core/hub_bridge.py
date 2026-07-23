import time

from core.event_bus import bus

from core.genesis.mission_result_memory import (
    mission_result_memory
)


class HubBridge:


    def __init__(self):

        self.active_tasks = {}

        self.results = []

        print(
            "🔀 Genesis Hub Bridge Online"
        )


        bus.subscribe(
            "task",
            self.handle_task
        )

        bus.subscribe(
            "result",
            self.handle_result
        )

        bus.subscribe(
            "failure",
            self.handle_failure
        )



    async def handle_task(
        self,
        event: dict
    ):

        agent = event.get(
            "target"
        )


        print(
            f"🔀 [HUB] Routing {agent}"
        )


        self.active_tasks[
            event["id"]
        ] = {

            "agent": agent,

            "status":
                "PROCESSING",

            "started":
                time.time()

        }



    async def handle_result(
        self,
        event: dict
    ):


        print(
            "✅ [HUB] Result received"
        )


        stored = (
            mission_result_memory.store(
                event
            )
        )


        self.results.append(
            stored
        )


        task_id = (
            event.get(
                "payload",
                {}
            ).get(
                "task_id"
            )
        )


        if task_id:

            self.active_tasks[
                task_id
            ] = {

                "status":
                    "COMPLETED",

                "completed":
                    time.time()

            }




    async def handle_failure(
        self,
        event: dict
    ):


        print(
            f"⚠️ [HUB] Failure detected from {event.get('source')}"
        )


        await bus.publish(

            {

                "id":
                    f"retry_{event['id']}",

                "source":
                    "hub",

                "target":
                    "planner",

                "type":
                    "task",

                "payload":
                    {

                        "objective":
                            f"Recover failed task {event['id']}",

                        "priority":
                            "high"

                    }

            }

        )



hub_bridge = HubBridge()
