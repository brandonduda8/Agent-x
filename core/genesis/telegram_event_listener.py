import time

from core.genesis.event_stream import event_stream
from core.genesis.genesis_notification_engine import (
    genesis_notification_engine
)


class GenesisTelegramEventListener:


    def __init__(self):

        self.system = "GENESIS TELEGRAM EVENT LISTENER v1"

        self.connected = False



    def start(self):

        event_stream.subscribe(
            self.handle_event
        )

        self.connected = True


        return {

            "system":
            self.system,

            "status":
            "CONNECTED",

            "timestamp":
            time.time()

        }



    def handle_event(
        self,
        event
    ):

        return genesis_notification_engine.handle_event(
            event
        )



    def report(self):

        return {

            "system":
            self.system,

            "connected":
            self.connected,

            "timestamp":
            time.time()

        }



telegram_event_listener = GenesisTelegramEventListener()
