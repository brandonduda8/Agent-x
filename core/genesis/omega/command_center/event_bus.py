import time
import uuid
import json
import os


class GenesisOmegaEventBus:
    """
    GENESIS OMEGA EVENT BUS v1

    Central nervous system for Genesis Command Center.

    All agents publish events here.
    Dashboard consumes events from here.
    """

    def __init__(self):
        self.system = "GENESIS OMEGA EVENT BUS v1"

        self.events = []

        self.file = "data/genesis_omega_events.json"

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    self.events = json.load(f)
            except Exception:
                self.events = []


    def save(self):
        with open(self.file, "w") as f:
            json.dump(
                self.events,
                f,
                indent=2
            )


    def emit(
        self,
        event_type,
        source,
        message,
        data=None
    ):

        event = {
            "id":
                "event_" + uuid.uuid4().hex[:8],

            "type":
                event_type,

            "source":
                source,

            "message":
                message,

            "data":
                data or {},

            "timestamp":
                time.time()
        }


        self.events.append(event)

        self.save()

        print(
            "📡 Genesis Event:",
            event_type,
            source
        )

        return event



    def recent(self, limit=25):
        return self.events[-limit:]


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



genesis_event_bus = GenesisOmegaEventBus()
