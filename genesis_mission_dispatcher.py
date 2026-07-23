import time


class GenesisMissionDispatcher:

    def __init__(self):
        self.missions = []


    def assign_agent(self, category):

        agents = {
            "income": "Opportunity Discovery Agent",
            "revenue": "Revenue Agent",
            "housing": "Stability Agent",
            "development": "Development Agent"
        }

        return agents.get(category, "General Agent")


    def dispatch(self, actions):

        dispatched = []

        for action in actions:

            mission = {
                "mission_id": action["action_id"],
                "agent": self.assign_agent(action["category"]),
                "category": action["category"],
                "objective": action["objective"],
                "source_decision": action["source_decision"],
                "status": "DISPATCHED",
                "created": time.time()
            }

            self.missions.append(mission)
            dispatched.append(mission)


        return {
            "system": "GENESIS MISSION DISPATCHER v1",
            "status": "ONLINE",
            "missions_created": len(dispatched),
            "missions": dispatched,
            "timestamp": time.time()
        }


    def status(self):

        return {
            "system": "GENESIS MISSION DISPATCHER v1",
            "status": "ONLINE",
            "missions": self.missions,
            "count": len(self.missions),
            "timestamp": time.time()
        }


mission_dispatcher = GenesisMissionDispatcher()
