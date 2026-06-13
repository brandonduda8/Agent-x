from .event_bus import bus

class HubBridge:
    def __init__(self):
        self.active_tasks = {}
        bus.subscribe("task", self.handle_task)
        bus.subscribe("result", self.handle_result)
        bus.subscribe("failure", self.handle_failure)

    async def handle_task(self, event: dict):
        target = event['target']
        print(f"🔀 [HUB] Routing task '{event['id']}' to {target} agent...")
        self.active_tasks[event['id']] = "processing"

    async def handle_result(self, event: dict):
        task_id = event['payload'].get('task_id')
        self.active_tasks[task_id] = "completed"
        print(f"✅ [HUB] Task {task_id} completed. Notifying Monitor & Revenue agents.")
        await bus.publish({
            "id": f"opt_{task_id}",
            "source": "hub",
            "target": "monitor",
            "type": "optimization_trigger",
            "payload": {"task_id": task_id, "result": event['payload']}
        })

    async def handle_failure(self, event: dict):
        print(f"⚠️ [HUB] Failure detected in {event['source']}. Triggering recovery.")
        await bus.publish({
            "id": f"retry_{event['id']}",
            "source": "hub",
            "target": "planner",
            "type": "task",
            "payload": {"objective": f"Recover failed task: {event['id']}", "priority": "high"}
        })

bridge = HubBridge()
