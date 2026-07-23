import time


def outreach(context):

    leads = context.get(
        "leads",
        []
    )


    messages = []


    for lead in leads:

        messages.append(

            {
                "company":
                    lead["company"],

                "message":
                    (
                    "We help businesses automate "
                    "customer workflows with AI."
                    )

            }

        )


    return {

        "messages_created":
            len(messages),

        "messages":
            messages,

        "channel":
            "AI outreach",

        "timestamp":
            time.time()

    }
