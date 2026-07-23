import time
import uuid
import json
import os


class GenesisUnifiedEventFabric:

    def __init__(self):

        self.system = "GENESIS UNIFIED EVENT FABRIC v1"

        self.events = []

        self.listeners = {}

        self.memory_file = (
            "data/genesis_unified_events.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(self.memory_file):

            try:

                with open(
                    self.memory_file,
                    "r"
                ) as f:

                    self.events = json.load(f)

            except:

                self.events = []


    def save(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.events,
                f,
                indent=2
            )


    def subscribe(
        self,
        event_type,
        callback
    ):

        if event_type not in self.listeners:

            self.listeners[event_type] = []


        self.listeners[event_type].append(
            callback
        )


        return {
            "status": "SUBSCRIBED",
            "event": event_type
        }


    def publish(
        self,
        event_type,
        source,
        payload=None
    ):


        event = {

            "id":
                "fabric_" +
                uuid.uuid4().hex[:8],

            "type":
                event_type,

            "source":
                source,

            "payload":
                payload or {},

            "timestamp":
                time.time()

        }


        self.events.append(event)

        self.save()


        for listener in self.listeners.get(
            event_type,
            []
        ):

            try:

                listener(event)

            except Exception as e:

                print(
                    "Fabric listener error:",
                    e
                )


        print(
            f"🌐 FABRIC EVENT {event_type}"
        )


        return event



    def history(
        self,
        limit=50
    ):

        return self.events[-limit:]



    def report(self):

        return {

            "system":
                self.system,

            "events":
                len(self.events),

            "listeners":
                len(self.listeners),

            "timestamp":
                time.time()

        }



genesis_unified_event_fabric = (
    GenesisUnifiedEventFabric()
)
