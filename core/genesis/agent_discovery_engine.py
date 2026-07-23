import os
import json
import time
import uuid


class GenesisAgentDiscoveryEngine:

    def __init__(self):
        self.system = "GENESIS AGENT DISCOVERY ENGINE v1"

        self.search_paths = [
            "core",
            "agent-x-core",
            "digital-twin",
            "data",
            "deployment",
            "memory",
            "tasks"
        ]

        self.keywords = [
            "agent",
            "hermes",
            "golden",
            "claw",
            "zane",
            "open",
            "json",
            "genesis"
        ]

        self.output = "data/genesis_discovered_agents.json"


    def discover(self):

        discoveries = []

        for base in self.search_paths:

            if not os.path.exists(base):
                continue

            for root, dirs, files in os.walk(base):

                for filename in files:

                    lower = filename.lower()

                    if any(k in lower for k in self.keywords):

                        discoveries.append({
                            "id": "discovery_" + uuid.uuid4().hex[:8],
                            "source": os.path.join(root, filename),
                            "artifact": filename,
                            "timestamp": time.time()
                        })


        result = {
            "system": self.system,
            "agents_discovered": len(discoveries),
            "agents": discoveries,
            "timestamp": time.time()
        }


        os.makedirs("data", exist_ok=True)

        with open(self.output, "w") as f:
            json.dump(result, f, indent=2)


        print("🔎 Genesis Discovery Complete")
        print("Agents/artifacts found:", len(discoveries))

        return result


    def report(self):

        if os.path.exists(self.output):

            with open(self.output) as f:
                data = json.load(f)

            return {
                "system": self.system,
                "discoveries": data["agents_discovered"],
                "file": self.output,
                "timestamp": time.time()
            }

        return {
            "system": self.system,
            "discoveries": 0,
            "timestamp": time.time()
        }


agent_discovery_engine = GenesisAgentDiscoveryEngine()
