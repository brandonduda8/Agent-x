import time
import uuid

from core.genesis.memory.agent_memory import (
    agent_memory
)


class GenesisBusinessCycleMemoryBridge:

    def __init__(self):

        self.system = "GENESIS BUSINESS CYCLE MEMORY BRIDGE v1"
        self.records = []


    def record_cycle(
        self,
        cycle
    ):

        memory_record = {

            "id":
                "cycle_memory_" +
                uuid.uuid4().hex[:8],

            "mission":
                cycle.get(
                    "objective"
                ),

            "status":
                cycle.get(
                    "status"
                ),

            "execution":
                cycle.get(
                    "execution"
                ),

            "learning":
                cycle.get(
                    "learning"
                ),

            "timestamp":
                time.time()
        }


        agent_memory.learn(
            "Genesis CEO",
            memory_record
        )


        self.records.append(
            memory_record
        )


        print(
            "🧠 Business cycle stored permanently"
        )


        return memory_record


    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                len(self.records),

            "timestamp":
                time.time()
        }


business_cycle_memory_bridge = GenesisBusinessCycleMemoryBridge()
