import time


class GenesisSkillGapAnalyzer:


    def __init__(self):

        self.system = (
            "GENESIS SKILL GAP ANALYZER v1"
        )


    def analyze(
        self,
        required,
        available
    ):


        missing = [

            skill for skill in required

            if skill not in available

        ]


        return {

            "missing_skills":
                missing,

            "needs_evolution":
                len(missing) > 0,

            "timestamp":
                time.time()

        }
