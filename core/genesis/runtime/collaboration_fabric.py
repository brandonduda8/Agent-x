import time


class GenesisCollaborationFabric:


    def __init__(
        self,
        registry,
        messenger,
        teams
    ):

        self.registry = registry
        self.messenger = messenger
        self.teams = teams

        self.system = (
            "GENESIS MULTI-AGENT COLLABORATION FABRIC v1"
        )


    def register_agent(
        self,
        name,
        capabilities
    ):

        return self.registry.register(
            name,
            capabilities
        )


    def create_mission_team(
        self,
        mission,
        agents
    ):

        return self.teams.create_team(
            mission,
            agents
        )


    def communicate(
        self,
        sender,
        receiver,
        message
    ):

        return self.messenger.send(
            sender,
            receiver,
            message
        )
