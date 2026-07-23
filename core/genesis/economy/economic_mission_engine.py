import time
import uuid


class GenesisEconomicMissionEngine:
    """
    GENESIS ECONOMIC MISSION ENGINE v1

    Converts opportunities into executable economic missions.
    """

    def __init__(self):
        self.system = "GENESIS ECONOMIC MISSION ENGINE v1"
        self.missions = []

    def create_mission(
        self,
        objective,
        value_goal,
        skills
    ):

        mission = {
            "id": "mission_" + uuid.uuid4().hex[:8],
            "objective": objective,
            "value_goal": value_goal,
            "required_skills": skills,
            "status": "CREATED",
            "created": time.time()
        }

        self.missions.append(mission)

        print(
            f"💰 Economic mission created: {objective}"
        )

        return mission


    def activate(self, mission_id):

        for mission in self.missions:

            if mission["id"] == mission_id:

                mission["status"] = "ACTIVE"

                return mission

        return None


    def report(self):

        return {
            "system": self.system,
            "missions": len(self.missions),
            "active": [
                m for m in self.missions
                if m["status"] == "ACTIVE"
            ],
            "timestamp": time.time()
        }


economic_mission_engine = GenesisEconomicMissionEngine()
