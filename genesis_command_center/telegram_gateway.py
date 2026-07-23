import datetime
from telegram_adapter import TelegramAdapter


class TelegramGateway:

    def __init__(self):

        self.adapter = TelegramAdapter()
        self.pending = {}


    def create_approval(self, approval):

        self.pending[approval["id"]] = approval

        return self.adapter.approval_alert(approval)


    def process_command(self, command):

        parts = command.split()

        if len(parts) != 2:
            return {
                "status": "ERROR",
                "message": "Use APPROVE id or DENY id"
            }


        action = parts[0].upper()
        approval_id = int(parts[1])


        if approval_id not in self.pending:

            return {

                "status": "ERROR",

                "message": "Approval not found"

            }


        if action == "APPROVE":

            self.pending[approval_id]["status"] = "APPROVED"

        elif action == "DENY":

            self.pending[approval_id]["status"] = "DENIED"

        else:

            return {

                "status": "ERROR",

                "message": "Unknown command"

            }


        return {

            "approval": self.pending[approval_id],

            "timestamp": str(datetime.datetime.now())

        }



if __name__ == "__main__":


    gateway = TelegramGateway()


    approval = {

        "id": 7,

        "agent": "Revenue Agent",

        "action": "Send client outreach",

        "impact": "Possible revenue opportunity"

    }


    print(
        gateway.create_approval(approval)
    )


    print(
        gateway.process_command("APPROVE 7")
    )
