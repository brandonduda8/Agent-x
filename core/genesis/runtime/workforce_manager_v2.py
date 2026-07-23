import time
import uuid


class GenesisWorkforceManagerV2:


    def __init__(
        self,
        registry,
        matcher
    ):

        self.registry = registry

        self.matcher = matcher

        self.system = (
            "GENESIS WORKFORCE MANAGER v2"
        )


    def create_team(
        self,
        mission,
        capabilities
    ):


        agents = self.registry.available()


        selected = self.matcher.match(

            agents,

            capabilities

        )


        return {

            "id":
                "team_" +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "agents":
                selected["matches"],

            "status":
                "READY",

            "timestamp":
                time.time()

        }
