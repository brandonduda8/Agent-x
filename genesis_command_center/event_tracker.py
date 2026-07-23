import json
import datetime
import os


FILE = "events.json"


class EventTracker:

    def __init__(self):

        self.events = self.load()


    def load(self):

        if os.path.exists(FILE):

            with open(FILE,"r") as f:
                return json.load(f)

        return []


    def record(self, agent, action, result):

        event = {

            "agent":agent,

            "action":action,

            "result":result,

            "timestamp":
            str(datetime.datetime.now())

        }

        self.events.append(event)

        self.save()

        return event


    def save(self):

        with open(FILE,"w") as f:

            json.dump(
                self.events,
                f,
                indent=4
            )



if __name__ == "__main__":

    tracker = EventTracker()

    print(
        tracker.record(
            "Revenue Agent",
            "Generated outreach list",
            "50 leads prepared"
        )
    )
