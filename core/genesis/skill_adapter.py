import time


class GenesisSkillAdapter:

    def __init__(self):

        self.system = "GENESIS SKILL ADAPTER v1"

        self.upgrades = []


    def analyze_gap(
        self,
        required,
        available
    ):

        missing = [

            skill

            for skill in required

            if skill not in available

        ]


        result = {

            "missing_skills":
                missing,

            "timestamp":
                time.time()

        }


        self.upgrades.append(result)

        return result



    def recommend_agent(
        self,
        skill
    ):

        return {

            "skill":
                skill,

            "recommendation":
                "Create specialized Genesis worker"

        }


    def report(self):

        return {

            "system":
                self.system,

            "upgrades":
                len(self.upgrades),

            "timestamp":
                time.time()

        }


skill_adapter = GenesisSkillAdapter()
