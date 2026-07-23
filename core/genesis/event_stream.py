import time
import uuid


class GenesisEventStream:

    def __init__(self):

        self.system = "GENESIS EVENT STREAM v2"

        self.events = []

        self.listeners = []


    def emit(
        self,
        event_type,
        source,
        data=None
    ):

        event = {

            "id":
            "event_" + uuid.uuid4().hex[:8],

            "type":
            event_type,

            "source":
            source,

            "data":
            data or {},

            "timestamp":
            time.time()

        }


        self.events.append(event)


        print(
            f"📡 EVENT: {event_type} from {source}"
        )


        # Notify connected systems
        for listener in self.listeners:

            try:

                listener(event)

            except Exception as e:

                print(
                    "Listener error:",
                    str(e)
                )


        return event



    def subscribe(
        self,
        listener
    ):

        self.listeners.append(listener)

        return {

            "listener":
            str(listener),

            "status":
            "CONNECTED"

        }



    def latest(
        self,
        limit=10
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



event_stream = GenesisEventStream()
