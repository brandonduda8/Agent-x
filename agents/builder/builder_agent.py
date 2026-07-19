import asyncio

from core.event_bus import bus
from integrations.pure_graph_adapter import self_correcting_builder


class BuilderAgent:

    def __init__(self, name="Master-Builder"):

        self.name = name

        bus.subscribe(
            "task",
            self.on_task_received
        )


    async def on_task_received(self, event):

        if event.get("target") != "builder":
            return


        objective = event["payload"]["objective"]


        print(
            f"🛠️ [{self.name}] Received objective: {objective}"
        )

        print(
            "🔄 [PureGraph] Initiating self-correcting build loop..."
        )


        try:

            final_state = await self_correcting_builder.run(
                objective
            )


            if final_state.get("code_written"):

                print(
                    f"🎉 [{self.name}] Build successful!"
                )

                await self._report_success(
                    event["id"],
                    final_state["code_written"]
                )


            else:

                error = final_state.get(
                    "error_message",
                    "Unknown build failure"
                )


                print(
                    f"❌ [{self.name}] Failed: {error}"
                )


                await self._report_failure(
                    event["id"],
                    error
                )


        except Exception as e:

            print(
                f"❌ [{self.name}] Crash: {e}"
            )


            await self._report_failure(
                event["id"],
                str(e)
            )



    async def _report_success(
        self,
        task_id,
        artifacts
    ):

        await bus.publish({

            "id": f"res_{task_id}",

            "source": "builder",

            "target": "hub",

            "type": "result",

            "payload": {

                "task_id": task_id,

                "status": "success",

                "artifacts": artifacts

            }

        })



    async def _report_failure(
        self,
        task_id,
        error
    ):

        await bus.publish({

            "id": f"fail_{task_id}",

            "source": "builder",

            "target": "hub",

            "type": "failure",

            "payload": {

                "task_id": task_id,

                "error": error

            }

        })



builder = BuilderAgent()
