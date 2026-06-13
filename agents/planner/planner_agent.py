import asyncio
from core.event_bus import bus

class PlannerAgent:
    def __init__(self, name="Planner"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'planner':
            return
            
        print(f"🧠 [{self.name}] Analyzing objective: {event['payload']['objective']}")
        
        # Simulate breaking down the goal into subtasks
        subtasks = [
            {"id": f"task_{event['id']}_1", "target": "researcher", "objective": "Research market for AI automation micro-SaaS"},
            {"id": f"task_{event['id']}_2", "target": "builder", "objective": "Generate landing page code based on research"}
        ]
        
        for task in subtasks:
            await asyncio.sleep(1) # Simulate thinking time
            await bus.publish({
                "id": task["id"],
                "source": "planner",
                "target": task["target"],
                "type": "task",
                "payload": {"objective": task["objective"], "parent_id": event['id']}
            })

planner = PlannerAgent()
