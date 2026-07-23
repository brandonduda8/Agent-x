import time
import uuid
import json
import os


class GenesisEventBus:

    def __init__(self):

        self.system = "GENESIS EVENT BUS v1"

        self.events = []

        self.memory_file = (
            "data/genesis_event_bus.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )


        if os.path.exists(self.memory_file):

            try:
                with open(self.memory_file, "r") as f:
                    self.events = json.load(f)

            except Exception:
                self.events = []


    def publish(
        self,
        event_type,
        payload
    ):

        event = {

            "id":
                "event_" +
                uuid.uuid4().hex[:8],

            "type":
                event_type,

            "payload":
                payload,

            "timestamp":
                time.time()

        }


        self.events.append(event)

        self._save()

        return event



    def get_events(
        self,
        event_type=None
    ):

        if event_type:

            return [
                e for e in self.events
                if e["type"] == event_type
            ]

        return self.events



    def _save(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.events,
                f,
                indent=2
            )



    def report(self):

        return {

            "system":
                self.system,

            "events":
                len(self.events),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_event_bus = GenesisEventBus()
