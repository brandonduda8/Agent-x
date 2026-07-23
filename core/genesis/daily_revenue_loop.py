import time
import uuid


class GenesisDailyRevenueLoop:
    """
    GENESIS DAILY REVENUE LOOP v1

    Finds and ranks revenue opportunities.
    """

    def __init__(self):
        self.system = "GENESIS DAILY REVENUE LOOP v1"
        self.cycles = 0
        self.missions = []


    def create_cycle(self, opportunities, profile):

        self.cycles += 1

        print(
            f"🧬 Revenue Cycle #{self.cycles} Started"
        )

        ranked = []

        user_skills = [
            skill.lower()
            for skill in profile.get(
                "skills",
                []
            )
        ]


        for opportunity in opportunities:

            opportunity_skills = [
                skill.lower()
                for skill in opportunity.get(
                    "skills",
                    []
                )
            ]

            matched_skills = [
                skill
                for skill in user_skills
                if skill in opportunity_skills
            ]

            value = opportunity.get(
                "value",
                opportunity.get(
                    "estimated_value",
                    0
                )
            )

            match_score = (
                len(matched_skills) * 20
            )

            revenue_score = min(
                value / 100,
                50
            )

            total_score = (
                match_score
                +
                revenue_score
            )


            ranked.append(
                {
                    "id":
                    "target_" +
                    uuid.uuid4().hex[:8],

                    "title":
                    opportunity.get(
                        "title"
                    ),

                    "value":
                    value,

                    "matched_skills":
                    matched_skills,

                    "score":
                    total_score,

                    "recommendation":
                    "EXECUTE"
                    if total_score >= 70
                    else "REVIEW"
                }
            )


            print(
                f"🎯 Opportunity Score: {total_score}% - "
                f"{ranked[-1]['recommendation']}"
            )


        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        mission = {

            "id":
            "daily_" +
            uuid.uuid4().hex[:8],

            "cycle":
            self.cycles,

            "targets":
            ranked,

            "status":
            "READY",

            "created":
            time.time()
        }


        self.missions.append(
            mission
        )


        print(
            "🔥 Revenue Cycle Complete"
        )


        return mission


    def report(self):

        return {
            "system":
            self.system,

            "cycles":
            self.cycles,

            "missions":
            len(
                self.missions
            ),

            "timestamp":
            time.time()
        }


daily_revenue_loop = GenesisDailyRevenueLoop()
