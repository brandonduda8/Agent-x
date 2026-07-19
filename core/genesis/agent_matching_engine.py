import time
import uuid


class GenesisAgentMatchingEngine:

    def __init__(self):

        self.system = "GENESIS AGENT MATCHING ENGINE v1"

        self.agents = {}

        self.matches = []



    def register_agent(
        self,
        name,
        skills
    ):

        agent = {

            "id":
                "agent_"
                +
                uuid.uuid4().hex[:8],

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
            f"🤖 Agent added to matcher: {name}"
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

            score = 0


            for skill in agent["skills"]:

                if skill in required:

                    score += 1


            if score > 0:

                scores[name] = score

                selected.append(
                    {
                        "agent": name,
                        "score": score,
                        "matched_skills":
                            [
                                s for s in agent["skills"]
                                if s in required
                            ]
                    }
                )



        result = {

            "id":
                "match_"
                +
                uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "team":
                selected,

            "scores":
                scores,

            "status":
                "READY",

            "timestamp":
                time.time()

        }


        self.matches.append(result)


        print(
            "🧬 Agent team selected"
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
