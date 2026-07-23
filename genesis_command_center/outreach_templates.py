import json
from datetime import datetime


def templates():

    return {

        "system": "GENESIS OUTREACH TEMPLATE ENGINE",

        "timestamp": str(datetime.now()),

        "templates": [

            {
                "name": "Initial Business Introduction",

                "purpose": "First contact with potential client",

                "requires_approval": True,

                "message":

                "Hello, I noticed your organization may benefit from improved automation and operational support. I would like to learn more about your current challenges and explore whether there is an opportunity to help."
            },


            {
                "name": "Follow Up Sequence",

                "purpose": "Re-engage previous contact",

                "requires_approval": True,

                "message":

                "I wanted to follow up and see if improving efficiency, customer communication, or workflow automation is currently a priority for your team."
            },


            {
                "name": "Partnership Opportunity",

                "purpose": "Create strategic relationships",

                "requires_approval": True,

                "message":

                "I am exploring potential partnerships where technology and automation can create measurable improvements. I would be interested in discussing possible collaboration."
            }

        ]
    }


if __name__ == "__main__":

    print(json.dumps(templates(), indent=4))
