import time
import uuid
import json
import os


class GenesisEvolutionManager:

    def __init__(self):

        self.name = "GENESIS EVOLUTION MANAGER v1"

        self.memory_path = (
            "core/genesis/data/genesis_memory.json"
        )

        self.evolution_path = (
            "core/genesis/data/genesis_evolution.json"
        )

        self.initialize()


    def initialize(self):

        directory = os.path.dirname(
            self.evolution_path
        )

        os.makedirs(
            directory,
            exist_ok=True
        )

        if not os.path.exists(
            self.evolution_path
        ):

            with open(
                self.evolution_path,
                "w"
            ) as f:

                json.dump(
                    {
                        "evolutions": []
                    },
                    f,
                    indent=2
                )


    def load_memory(self):

        if not os.path.exists(
            self.memory_path
        ):
            return []

        try:

            with open(
                self.memory_path,
                "r"
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):

                return data.get(
                    "memories",
                    []
                )

            return data

        except Exception:

            return []


    def save_evolution(
        self,
        evolution
    ):

        with open(
            self.evolution_path,
            "r"
        ) as f:

            data = json.load(f)


        data["evolutions"].append(
            evolution
        )


        with open(
            self.evolution_path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )


    def analyze_agent_performance(self):

        memories = self.load_memory()

        agents = {}


        for memory in memories:

            if not isinstance(
                memory,
                dict
            ):
                continue


            agent = memory.get(
                "agent",
                "Unknown"
            )


            score = memory.get(
                "score",
                0
            )


            if agent not in agents:

                agents[agent] = []

            agents[agent].append(
                score
            )


        report = []


        for agent, scores in agents.items():

            average = (
                sum(scores)
                /
                len(scores)
            )

            report.append(
                {
                    "agent": agent,
                    "average_score": average,
                    "runs": len(scores)
                }
            )


        return report



    def generate_agent_upgrade(
        self,
        agent,
        reason
    ):

        upgrade = {

            "id":
                "upgrade_" +
                uuid.uuid4().hex[:8],

            "agent":
                agent,

            "reason":
                reason,

            "recommended_changes":
                [
                    "Improve reasoning prompts",
                    "Add specialized knowledge",
                    "Increase task evaluation accuracy",
                    "Connect additional tools"
                ],

            "timestamp":
                time.time()
        }


        self.save_evolution(
            upgrade
        )


        return upgrade



    def create_specialized_agent(
        self,
        name,
        purpose,
        skills
    ):

        agent = {

            "id":
                "agent_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "purpose":
                purpose,

            "skills":
                skills,

            "created":
                time.time(),

            "status":
                "PROPOSED"

        }


        self.save_evolution(
            agent
        )


        return agent



    def get_evolution_report(self):

        if not os.path.exists(
            self.evolution_path
        ):

            return {
                "system": self.name,
                "evolutions": 0
            }


        with open(
            self.evolution_path,
            "r"
        ) as f:

            data = json.load(f)


        return {

            "system":
                self.name,

            "evolutions":
                len(
                    data.get(
                        "evolutions",
                        []
                    )
                ),

            "timestamp":
                time.time()
        }



genesis_evolution_manager = GenesisEvolutionManager()
