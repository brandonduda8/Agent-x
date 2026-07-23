import time

from core.genesis.mission_queue import mission_queue
from core.genesis.memory_engine import memory_engine


class GenesisMissionIntelligenceGuard:

    def __init__(self):
        self.system = "GENESIS MISSION INTELLIGENCE GUARD v1"


    def analyze(self, objective):

        missions = mission_queue.queue.get(
            "missions",
            []
        )

        active = [
            m for m in missions
            if m.get("status") == "ACTIVE"
        ]


        completed = [
            m for m in missions
            if m.get("status") == "COMPLETE"
        ]


        if active:

            return {
                "decision": "WAIT",
                "reason": "Existing mission active",
                "active_count": len(active),
                "timestamp": time.time()
            }


        previous = [
            m for m in completed
            if m.get("objective") == objective
        ]


        if previous:

            return {
                "decision": "IMPROVE",
                "reason": "Previous mission exists",
                "previous_results": len(previous),
                "timestamp": time.time()
            }


        return {
            "decision": "CREATE",
            "reason": "New opportunity",
            "timestamp": time.time()
        }



mission_intelligence_guard = GenesisMissionIntelligenceGuard()
