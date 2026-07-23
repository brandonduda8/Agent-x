import time
import uuid

from core.genesis.omega.command_center.mission_database import (
    genesis_mission_database
)


class GenesisOmegaMissionControlBridge:

    """
    GENESIS OMEGA MISSION CONTROL BRIDGE v2

    Live connection to Omega Mission Database.
    """

    def __init__(
        self,
        mission_database=None
    ):

        self.system = (
            "GENESIS OMEGA MISSION CONTROL BRIDGE v2"
        )

        self.mission_database = (
            mission_database
            or genesis_mission_database
        )

        self.snapshots = []


    def sync(self):

        missions = []


        if self.mission_database:

            try:

                missions = (
                    self.mission_database.list_all()
                )

            except Exception as e:

                missions = [
                    {
                        "error": str(e)
                    }
                ]


        snapshot = {

            "id":
                "mission_view_"
                + uuid.uuid4().hex[:8],

            "system":
                self.system,

            "missions":
                missions,

            "count":
                len(missions),

            "timestamp":
                time.time()

        }


        self.snapshots.append(
            snapshot
        )


        print(
            "📋 Mission Control Sync:",
            len(missions),
            "missions"
        )


        return snapshot



    def report(self):

        latest = self.sync()

        return {

            "system":
                self.system,

            "missions":
                latest["missions"],

            "count":
                latest["count"],

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_mission_control_bridge = (
    GenesisOmegaMissionControlBridge()
)
