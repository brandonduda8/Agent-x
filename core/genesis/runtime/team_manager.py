import time
import uuid


class GenesisTeamManager:


    def __init__(self):

        self.system = (
            "GENESIS TEAM MANAGER v1"
        )


    def create_team(
        self,
        mission,
        agents
    ):

        return {

            "id":
                "team_" +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "agents":
                agents,

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }
