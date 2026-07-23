import time
import uuid


class GenesisMetaGovernanceCouncil:


    def __init__(self):

        self.agents = []


    def register_agent(
        self,
        name,
        specialty,
        capabilities
    ):

        agent = {

            "id":
            "meta_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "specialty":
            specialty,

            "capabilities":
            capabilities,

            "status":
            "AVAILABLE",

            "timestamp":
            time.time()

        }


        self.agents.append(agent)


        return agent



    def assign(
        self,
        mission
    ):

        required = mission.get(
            "required_skill",
            ""
        )


        matches = []


        for agent in self.agents:

            if required in agent["capabilities"]:

                matches.append(agent)


        return {

            "mission":
            mission.get(
                "objective"
            ),

            "assigned_agents":
            matches,

            "status":
            "ASSIGNED"
            if matches
            else
            "NO_MATCH",

            "timestamp":
            time.time()

        }



    def council_status(self):

        return {

            "system":
            "GENESIS META GOVERNANCE COUNCIL v1",

            "agents":
            len(self.agents),

            "members":
            self.agents,

            "timestamp":
            time.time()

        }
