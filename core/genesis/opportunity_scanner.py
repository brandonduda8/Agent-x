import time
import uuid


class GenesisOpportunityScanner:
    """
    GENESIS OPPORTUNITY SCANNER v1

    Finds and ranks opportunities based on:

    - skill match
    - revenue potential
    - completion probability
    - Genesis capability
    """

    def __init__(self):

        self.system = "GENESIS OPPORTUNITY SCANNER v1"

        self.opportunities = []


    def add_opportunity(
        self,
        title,
        source,
        category,
        value,
        skills,
        description=""
    ):

        opportunity = {

            "id":
                "opp_" + uuid.uuid4().hex[:8],

            "title":
                title,

            "source":
                source,

            "category":
                category,

            "estimated_value":
                value,

            "skills":
                skills,

            "description":
                description,

            "status":
                "NEW",

            "created":
                time.time()

        }


        self.opportunities.append(
            opportunity
        )


        print(
            f"🎯 Opportunity Added: {title}"
        )


        return opportunity



    def scan(
        self,
        profile
    ):

        print(
            "🔎 Genesis scanning opportunities..."
        )


        results = []


        profile_skills = [
            skill.lower()
            for skill in profile.get(
                "skills",
                []
            )
        ]


        for opportunity in self.opportunities:

            job_skills = [

                skill.lower()

                for skill in opportunity.get(
                    "skills",
                    []
                )

            ]


            matched = []

            missing = []


            for skill in job_skills:

                if skill in profile_skills:

                    matched.append(
                        skill
                    )

                else:

                    missing.append(
                        skill
                    )


            if job_skills:

                match_score = int(
                    (
                        len(matched)
                        /
                        len(job_skills)
                    )
                    * 100
                )

            else:

                match_score = 0



            revenue_score = min(
                int(
                    opportunity.get(
                        "estimated_value",
                        0
                    )
                    /
                    100
                ),
                100
            )


            total_score = int(
                (
                    match_score * .7
                )
                +
                (
                    revenue_score * .3
                )
            )


            if total_score >= 80:

                recommendation = "APPLY_NOW"

            elif total_score >= 50:

                recommendation = "REVIEW"

            else:

                recommendation = "LOW_PRIORITY"



            result = {

                "id":
                    "scan_" + uuid.uuid4().hex[:8],

                "opportunity":
                    opportunity["title"],

                "source":
                    opportunity["source"],

                "match_score":
                    match_score,

                "revenue_score":
                    revenue_score,

                "total_score":
                    total_score,

                "matched_skills":
                    matched,

                "missing_skills":
                    missing,

                "recommendation":
                    recommendation,

                "timestamp":
                    time.time()

            }


            print(
                f"🧠 Opportunity Score: {total_score}% - {recommendation}"
            )


            results.append(
                result
            )


        return results



    def report(self):

        return {

            "system":
                self.system,

            "opportunities":
                len(
                    self.opportunities
                ),

            "timestamp":
                time.time()

        }



opportunity_scanner = GenesisOpportunityScanner()
