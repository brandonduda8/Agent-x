import time
import uuid


class GenesisEventBus:


    def __init__(self):

        self.events = []

        self.listeners = {}



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



    def publish(
        self,
        event_type,
        data
    ):


        event = {

            "id":
            "event_" + uuid.uuid4().hex[:8],

            "type":
            event_type,

            "data":
            data,

            "timestamp":
            time.time()

        }


        self.events.append(
            event
        )


        for listener in self.listeners.get(
            event_type,
            []
        ):

            listener(
                event
            )


        return event



    def history(
        self
    ):

        return self.events
