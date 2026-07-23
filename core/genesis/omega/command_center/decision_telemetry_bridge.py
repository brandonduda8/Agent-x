import time
import uuid


class GenesisOmegaDecisionTelemetryBridge:

    """
    GENESIS OMEGA DECISION TELEMETRY BRIDGE v1

    Converts AI decisions into observable
    Command Center events.
    """

    def __init__(
        self,
        event_bus=None
    ):

        self.system = (
            "GENESIS OMEGA DECISION TELEMETRY BRIDGE v1"
        )

        self.event_bus = event_bus
        self.events = []


    def publish_decision(
        self,
        decision
    ):

        event = {

            "id":
                "event_"
                + uuid.uuid4().hex[:8],

            "type":
                self._event_type(
                    decision
                ),

            "source":
                "DECISION_GATE",

            "message":
                decision.get(
                    "action"
                ),

            "data":
                {

                    "worker":
                        decision.get(
                            "worker"
                        ),

                    "risk":
                        decision.get(
                            "risk"
                        ),

                    "status":
                        decision.get(
                            "status"
                        )

                },

            "timestamp":
                time.time()

        }


        self.events.append(
            event
        )


        if self.event_bus:

            self.event_bus.publish(
                event
            )


        print(
            "📡 Decision Telemetry:",
            event["type"]
        )


        return event



    def _event_type(
        self,
        decision
    ):

        status = decision.get(
            "status"
        )


        if status == "WAITING_APPROVAL":

            return "APPROVAL_REQUIRED"


        if status == "AUTO_APPROVED":

            return "ACTION_AUTO_APPROVED"


        return "DECISION_CREATED"



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



genesis_decision_telemetry_bridge = (
    GenesisOmegaDecisionTelemetryBridge()
)
