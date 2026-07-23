import datetime


class TelegramAdapter:

    def __init__(self):

        self.name = "Telegram Operator Channel"
        self.status = "READY"


    def send(self, message):

        return {

            "channel": "telegram",

            "message": message,

            "timestamp": str(datetime.datetime.now()),

            "status": "QUEUED"

        }


    def approval_alert(self, approval):

        message = f"""
GENESIS APPROVAL REQUIRED

Agent:
{approval['agent']}

Action:
{approval['action']}

Impact:
{approval['impact']}

Reply:
APPROVE {approval['id']}
or
DENY {approval['id']}
"""

        return self.send(message)



if __name__ == "__main__":


    telegram = TelegramAdapter()


    test = {

        "id": 1,

        "agent": "Revenue Agent",

        "action": "Contact business lead",

        "impact": "Potential client opportunity"

    }


    print(
        telegram.approval_alert(test)
    )
