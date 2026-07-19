import time
import uuid


class GenesisCapabilityRegistry:

    def __init__(self):

        self.system = "GENESIS CAPABILITY REGISTRY v1"

        self.capabilities = []


    def register_capability(
        self,
        agent,
        capability,
        source="evolution"
    ):

        item = {

            "id":
                "capability_" + uuid.uuid4().hex[:8],

            "agent":
                agent,

            "capability":
                capability,

            "source":
                source,

            "status":
                "AVAILABLE",

            "created":
                time.time()
        }


        self.capabilities.append(item)


        print(
            f"🔧 Capability registered: {capability}"
        )


        return item



    def find_capabilities(
        self,
        agent
    ):

        return [

            item for item in self.capabilities

            if item["agent"] == agent

        ]



    def report(self):

        return {

            "system":
                self.system,

            "capabilities":
                len(self.capabilities),

            "timestamp":
                time.time()
        }



capability_registry = GenesisCapabilityRegistry()
