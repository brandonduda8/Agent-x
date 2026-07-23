import time
import uuid


from core.genesis.agent_registry import agent_registry



class GenesisAgentMatchingEngine:
    """
    GENESIS AGENT MATCHING ENGINE v4

    Persistent workforce intelligence.

    Automatically loads agents from:
    Genesis Persistent Agent Registry

    Flow:

    Agent Registry
          |
          v
    Matching Engine
          |
          v
    Mission Teams
    """



    def __init__(self):

        self.system = (
            "GENESIS AGENT MATCHING ENGINE v4"
        )

        self.agents = {}

        self.matches = []

        self.load_agents()



    def load_agents(self):

        for name, agent in agent_registry.agents.items():

            self.register_agent(
                name,
                agent.get(
                    "skills",
                    []
                )
            )



    def register_agent(
        self,
        name,
        skills
    ):


        agent = {

            "id":
            "agent_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "skills":
            skills,

            "status":
            "AVAILABLE",

            "registered":
            time.time()

        }


        self.agents[name] = agent


        print(
            f"🤖 Agent registered: {name}"
        )


        return agent



    def match(
        self,
        mission
    ):


        required = mission.get(
            "required_capabilities",
            []
        )


        selected = []

        scores = {}



        for name, agent in self.agents.items():

            matched = [

                skill

                for skill in agent["skills"]

                if skill in required

            ]


            score = len(matched)


            if score > 0:

                scores[name] = score


                selected.append({

                    "agent":
                    name,

                    "score":
                    score,

                    "matched_skills":
                    matched

                })



        result = {

            "id":
            "match_" + uuid.uuid4().hex[:8],

            "mission":
            mission.get("id"),

            "team":
            selected,

            "scores":
            scores,

            "status":
            "READY",

            "timestamp":
            time.time()

        }


        self.matches.append(
            result
        )


        print(
            "🧬 Dynamic agent team selected"
        )


        return result



    def report(self):

        return {

            "system":
            self.system,

            "agents":
            len(self.agents),

            "matches":
            len(self.matches),

            "timestamp":
            time.time()

        }



agent_matching_engine = GenesisAgentMatchingEngine()
