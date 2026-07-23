import time


class GenesisAssignmentEngine:


    def assign(
        self,
        mission,
        agents
    ):

        return {

            "mission":
            mission,

            "assigned_agents":
            agents,

            "status":
            "ASSIGNED",

            "timestamp":
            time.time()

        }
