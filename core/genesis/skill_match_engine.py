import time
import uuid


class GenesisSkillMatchEngine:
    """
    GENESIS SKILL MATCH ENGINE v1

    Evaluates jobs against Genesis capabilities.

    Converts:
        Job
          |
          v
    Capability Analysis
          |
          v
    Success Probability
          |
          v
    Application Priority
    """

    def __init__(self):

        self.system = (
            "GENESIS SKILL MATCH ENGINE v1"
        )

        self.profile = {

            "skills": [

                "Python",
                "AI agents",
                "automation",
                "APIs",
                "backend development",
                "workflow automation",
                "sales automation",
                "LLM systems"

            ],

            "experience_level":
                "builder",

            "projects":

                [

                    "Genesis AI Agent System",
                    "Revenue Automation Engine",
                    "Autonomous Multi-Agent Framework"

                ]

        }

        self.matches = []



    def evaluate(self, job):

        required = job.get(
            "skills",
            []
        )


        matched = []

        missing = []


        for skill in required:

            found = False


            for my_skill in self.profile["skills"]:

                if (
                    skill.lower()
                    in my_skill.lower()

                    or

                    my_skill.lower()
                    in skill.lower()
                ):

                    found = True
                    break


            if found:

                matched.append(skill)

            else:

                missing.append(skill)



        score = 0


        if required:

            score = int(
                (
                    len(matched)
                    /
                    len(required)
                )
                *
                100
            )



        if score >= 80:

            recommendation = "APPLY_NOW"

        elif score >= 50:

            recommendation = "BUILD_PORTFOLIO_FIRST"

        else:

            recommendation = "LOW_PRIORITY"



        result = {


            "id":
                "match_"
                +
                uuid.uuid4().hex[:8],


            "job":
                job["title"],


            "company":
                job["company"],


            "match_score":
                score,


            "matched_skills":
                matched,


            "missing_skills":
                missing,


            "recommendation":
                recommendation,


            "timestamp":
                time.time()

        }


        self.matches.append(result)


        print(
            f"🧠 Job Match: {score}% - {recommendation}"
        )


        return result




    def analyze_jobs(self, jobs):

        results = []


        for job in jobs:

            results.append(
                self.evaluate(job)
            )


        return results




    def report(self):

        return {

            "system":
                self.system,

            "matches":
                len(self.matches),

            "timestamp":
                time.time()

        }



skill_match_engine = GenesisSkillMatchEngine()
