import time
import uuid


class GenesisIntelligenceMesh:
    """
    GENESIS INTELLIGENCE MESH v1

    Unified intelligence layer connecting:
    - agents
    - tools
    - events
    - missions
    - system health
    """

    def __init__(
        self,
        agent_registry=None,
        agent_manager=None,
        event_stream=None,
        tool_registry=None,
        kernel=None
    ):

        self.id = "mesh_" + uuid.uuid4().hex[:8]
        self.system = "GENESIS INTELLIGENCE MESH v1"

        self.agent_registry = agent_registry
        self.agent_manager = agent_manager
        self.event_stream = event_stream
        self.tool_registry = tool_registry
        self.kernel = kernel

        self.running = False
        self.started = None

    def start(self):

        self.running = True
        self.started = time.time()

        print("""
================================
🧬 GENESIS INTELLIGENCE MESH ONLINE
================================
""")

        if self.event_stream:
            self.event_stream.emit(
                "INTELLIGENCE_MESH_STARTED",
                self.system
            )

        return self.report()


    def discover_agents(self):

        result = {}

        if self.agent_registry:
            result["registry"] = (
                self.agent_registry.report()
            )

        if self.agent_manager:
            result["manager"] = (
                self.agent_manager.health_report()
            )

        return result


    def discover_tools(self):

        if self.tool_registry:
            return self.tool_registry.report()

        return {
            "tools":0
        }


    def recent_events(self, limit=10):

        if self.event_stream:
            return self.event_stream.latest(limit)

        return []


    def assign_task(self, objective):

        mission = {
            "id":
                "mission_" + uuid.uuid4().hex[:8],
            "objective":
                objective,
            "status":
                "CREATED",
            "created":
                time.time()
        }

        if self.event_stream:
            self.event_stream.emit(
                "MISSION_CREATED",
                self.system,
                mission
            )

        return mission


    def health(self):

        return {
            "status":
                "ONLINE" if self.running else "OFFLINE",
            "agents":
                len(
                    self.discover_agents()
                ),
            "tools":
                self.discover_tools().get(
                    "tools",
                    0
                ),
            "events":
                len(
                    self.recent_events()
                ),
            "timestamp":
                time.time()
        }


    def report(self):

        return {
            "id":
                self.id,
            "system":
                self.system,
            "running":
                self.running,
            "agents":
                self.discover_agents(),
            "tools":
                self.discover_tools(),
            "events":
                self.recent_events(),
            "health":
                self.health(),
            "timestamp":
                time.time()
        }
