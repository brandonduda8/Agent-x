import asyncio
from core.event_bus import bus
from integrations.pure_graph_adapter import self_correcting_builder

class BuilderAgent:
    def __init__(self, name="Master-Builder"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'builder':
            return
            
        objective = event['payload']['objective']
        print(f"🛠️ [{self.name}] Received objective: {objective}")
        print("🔄 [PureGraph] Initiating self-correcting build loop...")
        
        try:
            # Run the Pure Python State Machine
            final_state = await self_correcting_builder.run(objective)
            
            # Check if it succeeded or failed after all iterations
            if final_state.get('error_message') and not final_state.get('code_written'):
                print(f"❌ [{self.name}] Failed after {final_state['iteration_count']} attempts: {final_state['error_message']}")
                await self._report_failure(event['id'], final_state['error_message'])
            else:
                print(f"🎉 [{self.name}] Build successful! Artifacts: {final_state['code_written']}")
                await self._report_success(event['id'], final_state['code_written'])
                
        except Exception as e:
            print(f"❌ [{self.name}] PureGraph crashed: {e}")
            await self._report_failure(event['id'], str(e))

    async def _report_success(self, task_id: str, artifacts: list):
        await bus.publish({
            "id": f"res_{task_id}",
            "source": "builder",
            "target": "hub",
            "type": "result",
            "payload": {"task_id": task_id, "status": "success", "artifacts": artifacts}
        })

    async def _report_failure(self, task_id: str, error: str):
        await bus.publish({
            "id": f"fail_{task_id}",
            "source": "builder",
            "target": "hub",
            "type": "failure",
            "payload": {"task_id": task_id, "error": error}
        })

builder = BuilderAgent()
