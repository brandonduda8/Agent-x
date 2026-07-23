import time


class GenesisMissionPriorityEngine:

    def __init__(self):
        self.system = "GENESIS MISSION PRIORITY ENGINE v1"

    def prioritize(self, missions):

        ranked = []

        for mission in missions:

            score = 0

            if "income" in mission["mission"].lower():
                score += 5

            if "work" in mission["mission"].lower():
                score += 5

            if "housing" in mission["mission"].lower():
                score += 5

            if "Coordinate" in mission["mission"]:
                score += 2

            ranked.append({
                "agent": mission["agent"],
                "mission": mission["mission"],
                "priority_score": score,
                "status": "READY"
            })

        ranked.sort(
            key=lambda x: x["priority_score"],
            reverse=True
        )

        return {
            "system": self.system,
            "status": "ONLINE",
            "ranked_missions": ranked,
            "timestamp": time.time()
        }


genesis_mission_priority_engine = GenesisMissionPriorityEngine()
