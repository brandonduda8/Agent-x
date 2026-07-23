import time


class GenesisOpportunityAnalyzer:


    def score(
        self,
        problem,
        value,
        industry
    ):

        pain_score = 0
        revenue_score = 0
        automation_score = 0
        access_score = 0


        # Problem urgency

        if any(word in problem.lower()
               for word in [
                   "lost",
                   "missed",
                   "slow",
                   "leads",
                   "appointments"
               ]):

            pain_score = 25

        else:

            pain_score = 15


        # Revenue potential

        if value >= 1000:

            revenue_score = 25

        elif value >= 500:

            revenue_score = 20

        else:

            revenue_score = 10


        # Automation fit

        automation_industries = [

            "dental",
            "hvac",
            "restaurant",
            "real estate",
            "medical"

        ]


        if industry.lower() in automation_industries:

            automation_score = 25

        else:

            automation_score = 15


        # Reachability

        access_score = 20


        total = (

            pain_score +
            revenue_score +
            automation_score +
            access_score

        )


        priority = "LOW"


        if total >= 80:

            priority = "HIGH"

        elif total >= 60:

            priority = "MEDIUM"


        return {

            "industry":
            industry,

            "score":
            total,

            "priority":
            priority,

            "reason":
            [
                "Problem urgency evaluated",
                "Revenue potential evaluated",
                "Automation fit evaluated"
            ],

            "recommended_action":
            "Create sales mission"
            if total >= 70
            else
            "Continue research",

            "timestamp":
            time.time()

        }
