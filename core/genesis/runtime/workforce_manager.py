import time
import uuid


class GenesisWorkforceManager:


    def __init__(
        self,
        registry=None,
        harness=None
    ):

        self.system = (
            "GENESIS WORKFORCE MANAGER v1"
        )

        self.registry = registry

        self.harness = harness

        self.workforce = {}



    def add_agent(
        self,
        agent
    ):

        self.workforce[
            agent.name
        ] = agent


        if self.harness:

            self.harness.register(
                agent
            )


        return {

            "agent":
                agent.name,

            "status":
                "ADDED"

        }



    def find_workers(
        self,
        capability
    ):

        matches = []


        for agent in self.workforce.values():

            if capability in agent.capabilities:

                matches.append(agent.name)


        return matches



    def build_team(
        self,
        requirements
    ):

        team = []


        for requirement in requirements:

            workers = self.find_workers(
                requirement
            )

            team.extend(workers)


        return {

            "id":
                "team_" +
                uuid.uuid4().hex[:8],

            "requirements":
                requirements,

            "agents":
                list(set(team)),

            "created":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.workforce),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
