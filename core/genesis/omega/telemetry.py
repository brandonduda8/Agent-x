import time

from core.genesis.omega.command_center.event_bus import (
    genesis_event_bus
)


class GenesisOmegaTelemetry:

    """
    GENESIS OMEGA TELEMETRY SYSTEM v1

    Observability layer for all autonomous activity.
    """

    def __init__(self):
        self.system = (
            "GENESIS OMEGA TELEMETRY SYSTEM v1"
        )

        self.events = []


    def record(
        self,
        event_type,
        source,
        message,
        data=None
    ):

        event = genesis_event_bus.emit(
            event_type,
            source,
            message,
            data or {}
        )

        self.events.append(event)

        return event


    def mission_started(
        self,
        objective
    ):

        return self.record(
            "MISSION_STARTED",
            "OMEGA_CONTROLLER",
            objective
        )


    def worker_activity(
        self,
        capability,
        result
    ):

        return self.record(
            "WORKER_ACTIVITY",
            capability,
            "Worker execution completed",
            result
        )


    def learning_update(
        self,
        data
    ):

        return self.record(
            "LEARNING_UPDATE",
            "OMEGA_LEARNING_LOOP",
            "Learning pattern created",
            data
        )


    def report(self):

        return {
            "system": self.system,
            "events": len(self.events),
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_omega_telemetry = GenesisOmegaTelemetry()
