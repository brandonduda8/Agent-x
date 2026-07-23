import time


class GenesisNotificationEngine:

    """
    GENESIS NOTIFICATION ENGINE v1

    Converts Genesis events into human alerts.
    """

    def __init__(
        self,
        telegram_bridge=None
    ):

        self.system = "GENESIS NOTIFICATION ENGINE v1"

        self.telegram_bridge = telegram_bridge

        self.notifications = []


    def handle_event(
        self,
        event
    ):

        event_type = event.get(
            "type",
            "UNKNOWN"
        )

        source = event.get(
            "source",
            "Genesis"
        )

        message = (
            "🧬 GENESIS EVENT\n\n"
            f"Type:\n{event_type}\n\n"
            f"Source:\n{source}\n\n"
            "Status:\nRECEIVED"
        )


        notification = {

            "event":
            event,

            "message":
            message,

            "timestamp":
            time.time()

        }


        self.notifications.append(
            notification
        )


        if self.telegram_bridge:

            try:

                self.telegram_bridge.send(
                    message
                )

            except Exception:

                pass


        print(
            message
        )


        return notification



    def report(self):

        return {

            "system":
            self.system,

            "notifications":
            len(self.notifications),

            "timestamp":
            time.time()

        }



genesis_notification_engine = GenesisNotificationEngine()
