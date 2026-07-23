import time


def lead_generation(context):

    prospects = context.get(
        "prospects",
        []
    )


    leads = []

    for prospect in prospects:

        leads.append(

            {
                "company":
                    prospect["company"],

                "contact_status":
                    "NEW",

                "lead_score":
                    prospect["automation_score"]

            }

        )


    return {

        "leads":
            leads,

        "count":
            len(leads),

        "timestamp":
            time.time()

    }
