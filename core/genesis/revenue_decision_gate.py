import time
import uuid

from core.genesis.mission_cycle_guard import (
    mission_cycle_guard
)

from core.genesis.mission_queue import (
    mission_queue
)


class GenesisRevenueDecisionGate:
    """
    GENESIS REVENUE DECISION GATE v1

    Controls autonomous revenue execution.

    Responsibilities:
    - prevent duplicate revenue loops
    - check mission queue
    - approve new revenue missions
    - create execution permission
    """

    def __init__(self):
        self.system = (
            "GENESIS REVENUE DECISION GATE v1"
        )

        self.decisions = []


    def check_duplicate(self, objective):

        allowed = mission_cycle_guard.allow(
            objective
        )

        return allowed


    def check_queue(self):

        active = [
            m
            for m in mission_queue.queue["missions"]
            if m["status"] in [
                "QUEUED",
                "ACTIVE"
            ]
        ]

        return len(active)


    def authorize(self, objective):

        existing = self.check_queue()

        if existing > 0:

            decision = {
                "status": "BLOCKED",
                "reason": "Existing missions active",
                "objective": objective
            }

            self.decisions.append(decision)

            return decision


        if not self.check_duplicate(objective):

            decision = {
                "status": "BLOCKED",
                "reason": "Duplicate mission cooldown",
                "objective": objective
            }

            self.decisions.append(decision)

            return decision


        decision = {
            "id":
                "decision_"
                + uuid.uuid4().hex[:8],

            "status": "APPROVED",

            "objective": objective,

            "timestamp": time.time()
        }


        self.decisions.append(decision)


        print(
            "✅ Revenue mission approved"
        )


        return decision



    def report(self):

        return {

            "system": self.system,

            "decisions":
                len(self.decisions),

            "timestamp":
                time.time()
        }



revenue_decision_gate = (
    GenesisRevenueDecisionGate()
)
