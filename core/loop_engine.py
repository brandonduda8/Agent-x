import asyncio
import time
import random

from core.revenue_engine import RevenueEngine
from core.revenue_brain import RevenueBrain


class LoopEngine:

    def __init__(self, hub, tasks, supervisor):

        self.hub = hub
        self.tasks = tasks
        self.supervisor = supervisor

        # Revenue system (v3.1 brain layer)
        self.revenue = RevenueEngine()
        self.revenue_brain = RevenueBrain(self.revenue)

        self.running = True
        self.cycle_delay = 2

    # -------------------------
    # MAIN LOOP
    # -------------------------
    async def start(self):

        print("[LOOP v3.1 STARTED - REVENUE INTELLIGENCE ACTIVE]")

        while self.running:

            await self.cycle()

            await asyncio.sleep(self.cycle_delay)

    # -------------------------
    # SINGLE CYCLE
    # -------------------------
    async def cycle(self):

        self.supervisor.stats["events"] += 1

        tasks = self.tasks.list()

        # If no tasks → generate goal
        if not tasks:

            await self.generate_goal()
            return

        # Rank tasks using revenue brain
        ranked_tasks = self.revenue_brain.rank(tasks)

        for task in list(ranked_tasks):

            await self.execute_task(task)

            # remove after execution
            if task in tasks:
                tasks.remove(task)

        self.tasks.save(tasks)

    # -------------------------
    # GOAL GENERATION
    # -------------------------
    async def generate_goal(self):

        goals = [
            "build monetization feature",
            "improve automation system",
            "create revenue tool",
            "optimize agent workflow",
            "expand system capabilities"
        ]

        goal = {
            "type": "goal",
            "objective": random.choice(goals),
            "timestamp": time.time()
        }

        print("[LOOP] GENERATED GOAL:", goal["objective"])

        await self.hub.send(
            "system",
            "planner",
            "goal",
            goal
        )

    # -------------------------
    # EXECUTE TASK
    # -------------------------
    async def execute_task(self, task):

        print("[LOOP] EXECUTING:", task)

        try:

            # route to builder
            if task["type"] == "build":

                await self.hub.send(
                    "loop",
                    "builder",
                    "build",
                    task["data"]
                )

                # REVENUE SIGNAL (SUCCESS)
                self.revenue.add(
                    source="task_success",
                    amount=1,
                    meta=task
                )

                self.supervisor.task_done()

            else:

                # REVENUE SIGNAL (NON-BUILD / FAILURE TYPE)
                self.revenue.add(
                    source="task_unhandled",
                    amount=0,
                    meta=task
                )

                self.supervisor.task_failed()

        except Exception as e:

            print("[LOOP ERROR]", e)

            # FAILURE SIGNAL
            self.revenue.add(
                source="task_error",
                amount=0,
                meta=task
            )

            self.supervisor.task_failed()

    # -------------------------
    # STOP LOOP
    # -------------------------
    def stop(self):

        self.running = False
