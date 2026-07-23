import time
import uuid
import json
import os


class GenesisAgentFactory:

    def __init__(self):

        self.name = "GENESIS AGENT FACTORY v1"

        self.registry_path = (
            "core/genesis/data/genesis_agents.json"
        )

        self.initialize()


    def initialize(self):

        directory = os.path.dirname(
            self.registry_path
        )

        os.makedirs(
            directory,
            exist_ok=True
        )

        if not os.path.exists(
            self.registry_path
        ):

            with open(
                self.registry_path,
                "w"
            ) as f:

                json.dump(
                    {
                        "agents": []
                    },
                    f,
                    indent=2
                )


    def load_agents(self):

        try:

            with open(
                self.registry_path,
                "r"
            ) as f:

                data = json.load(f)

            return data.get(
                "agents",
                []
            )

        except Exception:

            return []


    def save_agents(
        self,
        agents
    ):

        with open(
            self.registry_path,
            "w"
        ) as f:

            json.dump(
                {
                    "agents": agents
                },
                f,
                indent=2
            )


    def create_agent_blueprint(
        self,
        name,
        role,
        skills,
        mission
    ):

        agent = {

            "id":
                "agent_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "role":
                role,

            "skills":
                skills,

            "mission":
                mission,

            "status":
                "PROPOSED",

            "created":
                time.time()

        }


        agents = self.load_agents()

        agents.append(
            agent
        )

        self.save_agents(
            agents
        )


        return agent



    def discover_capability_gap(
        self,
        missing_skill
    ):

        return {

            "id":
                "gap_" +
                uuid.uuid4().hex[:8],

            "missing_capability":
                missing_skill,

            "recommendation":
                "Create specialized Genesis agent",

            "timestamp":
                time.time()

        }



    def get_agent_report(self):

        agents = self.load_agents()

        return {

            "system":
                self.name,

            "registered_agents":
                len(agents),

            "agents":
                agents,

            "timestamp":
                time.time()

        }



genesis_agent_factory = GenesisAgentFactory()
