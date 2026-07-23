import time


def market_research(context):

    objective = context.get(
        "objective",
        ""
    )


    prospects = [

        {
            "company":
                "Local Dental Practice",

            "industry":
                "Healthcare",

            "pain_points":
                [
                    "missed calls",
                    "manual scheduling",
                    "slow follow ups"
                ],

            "automation_score":
                95
        },

        {
            "company":
                "Real Estate Agency",

            "industry":
                "Real Estate",

            "pain_points":
                [
                    "lead response delays",
                    "manual CRM updates"
                ],

            "automation_score":
                90
        }

    ]


    return {

        "objective":
            objective,

        "prospects":
            prospects,

        "count":
            len(prospects),

        "generated":
            time.time()

    }
