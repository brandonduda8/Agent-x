import json
import datetime
import os


COMMUNICATION_FILE = "communication_queue.json"


class CommunicationLayer:

    def __init__(self):
        self.queue = self.load()

    def load(self):

        if os.path.exists(COMMUNICATION_FILE):
            with open(COMMUNICATION_FILE, "r") as f:
                return json.load(f)

        return {
            "notifications": [],
            "approvals": [],
            "daily_briefs": []
        }


    def save(self):

        with open(COMMUNICATION_FILE, "w") as f:
            json.dump(self.queue, f, indent=4)


    def notify(self, title, message, priority="NORMAL"):

        alert = {
            "type": "NOTIFICATION",
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": str(datetime.datetime.now())
        }

        self.queue["notifications"].append(alert)

        self.save()

        return alert


    def request_approval(self, action, reason):

        approval = {
            "type": "APPROVAL_REQUIRED",
            "action": action,
            "reason": reason,
            "status": "WAITING",
            "timestamp": str(datetime.datetime.now())
        }

        self.queue["approvals"].append(approval)

        self.save()

        return approval


    def create_daily_brief(self, focus, actions):

        brief = {
            "type": "DAILY_POWER_BRIEF",
            "focus": focus,
            "actions": actions,
            "timestamp": str(datetime.datetime.now())
        }

        self.queue["daily_briefs"].append(brief)

        self.save()

        return brief



if __name__ == "__main__":

    comms = CommunicationLayer()


    print(
        comms.notify(
            "Genesis Online",
            "All core systems connected",
            "HIGH"
        )
    )


    print(
        comms.request_approval(
            "Launch outreach campaign",
            "Potential revenue opportunity identified"
        )
    )


    print(
        comms.create_daily_brief(
            "Business Development",
            [
                "Review new leads",
                "Send approved outreach",
                "Update pipeline"
            ]
        )
    )
