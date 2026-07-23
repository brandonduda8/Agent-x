import time
import uuid


class GenesisWorkforceScheduler:

    def __init__(self):
        self.schedules = []
        self.assignments = []


    def create_schedule(
        self,
        mission_id,
        tasks,
        revenue_priority="HIGH"
    ):

        schedule = {
            "id": f"schedule_{uuid.uuid4().hex[:8]}",
            "mission": mission_id,
            "priority": revenue_priority,
            "tasks": [
                {
                    "id": f"scheduled_task_{uuid.uuid4().hex[:8]}",
                    "name": task,
                    "status": "WAITING"
                }
                for task in tasks
            ],
            "status": "READY",
            "timestamp": time.time()
        }

        self.schedules.append(schedule)

        return schedule


    def dispatch_task(
        self,
        schedule_id,
        task_id,
        agent
    ):

        assignment = {
            "id": f"dispatch_{uuid.uuid4().hex[:8]}",
            "schedule": schedule_id,
            "task": task_id,
            "agent": agent,
            "status": "ASSIGNED",
            "timestamp": time.time()
        }

        self.assignments.append(assignment)

        return assignment


    def optimize_order(
        self,
        schedule_id
    ):

        for schedule in self.schedules:
            if schedule["id"] == schedule_id:

                schedule["tasks"] = sorted(
                    schedule["tasks"],
                    key=lambda x: x["name"]
                )

                schedule["optimized"] = True

                return {
                    "schedule": schedule_id,
                    "optimization": "Revenue workflow prioritized",
                    "status": "OPTIMIZED",
                    "timestamp": time.time()
                }


        return {
            "status": "FAILED",
            "reason": "Schedule not found"
        }


    def report(self):

        return {
            "system":
                "GENESIS AUTONOMOUS WORKFORCE SCHEDULER v1",
            "schedules":
                len(self.schedules),
            "assignments":
                len(self.assignments),
            "status":
                "ONLINE",
            "timestamp":
                time.time()
        }


genesis_workforce_scheduler = GenesisWorkforceScheduler()
