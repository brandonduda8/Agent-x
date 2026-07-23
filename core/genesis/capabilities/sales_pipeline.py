import time


def sales_pipeline(context):

    leads = context.get(
        "leads",
        []
    )


    return {

        "pipeline":

            [

                {
                    "company":
                        lead["company"],

                    "stage":
                        "PROSPECT"

                }

                for lead in leads

            ],

        "timestamp":
            time.time()

    }
