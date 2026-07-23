import time
import uuid


class GenesisRealityMissionController:

    name = "GENESIS REALITY MISSION CONTROLLER v2"

    def __init__(self):
        self.missions = []

    def create_mission(self, objective, agent, priority):

        mission = {
            "id": f"mission_{uuid.uuid4().hex[:8]}",
            "objective": objective,
            "assigned_agent": agent,
            "priority": priority,
            "status": "READY",
            "actions": [],
            "created": time.time()
        }

        self.missions.append(mission)

        return mission

    def add_action(self, mission_id, action):

        for mission in self.missions:
            if mission["id"] == mission_id:
                mission["actions"].append({
                    "action": action,
                    "timestamp": time.time()
                })
                return mission

        return {
            "status": "MISSION_NOT_FOUND"
        }

    def report(self):

        return {
            "system": self.name,
            "status": "ONLINE",
            "missions": self.missions,
            "count": len(self.missions),
            "timestamp": time.time()
        }


genesis_reality_mission_controller = GenesisRealityMissionController()
