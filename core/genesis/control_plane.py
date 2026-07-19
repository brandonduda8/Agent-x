import time
import uuid


class GenesisControlPlane:
    """
    GENESIS CONTROL PLANE v1

    Executive coordination layer responsible for:
    - connecting Genesis subsystems
    - unified system reporting
    - mission coordination
    - capability visibility
    """

    def __init__(
        self,
        kernel=None,
        controller=None,
        tools=None
    ):
        self.id = "control_" + uuid.uuid4().hex[:8]
        self.system = "GENESIS CONTROL PLANE v1"

        self.kernel = kernel
        self.controller = controller
        self.tools = tools

        self.systems = {}
        self.missions = []

        self.running = False
        self.started = None

    def register_system(self, name, system):
        self.systems[name] = {
            "system": system,
            "status": "CONNECTED",
            "timestamp": time.time()
        }

        print(f"🧬 Control Plane connected: {name}")

        return {
            "status": "CONNECTED",
            "system": name
        }

    def register_agent(self, name, agent):
        if self.kernel:
            return self.kernel.register_agent(name, agent)

        return {
            "status": "NO_KERNEL",
            "agent": name
        }

    def create_mission(self, objective):
        mission = {
            "id": "mission_" + uuid.uuid4().hex[:8],
            "objective": objective,
            "status": "READY",
            "agents": [],
            "created": time.time()
        }

        if self.controller:
            controller_mission = self.controller.mission(objective)
            mission.update(controller_mission)

        self.missions.append(mission)

        print(
            f"🚀 Mission created: {objective}"
        )

        return mission

    def discover_capabilities(self):
        if self.tools:
            return self.tools.report()

        return {
            "tools": 0,
            "status": "NO_TOOL_REGISTRY"
        }

    def start(self):
        self.running = True
        self.started = time.time()

        print("""
================================
🧬 GENESIS CONTROL PLANE ONLINE
================================
""")

        return self.report()

    def health(self):
        return {
            "status": "ONLINE" if self.running else "OFFLINE",
            "systems": len(self.systems),
            "missions": len(self.missions),
            "timestamp": time.time()
        }

    def report(self):
        return {
            "id": self.id,
            "system": self.system,
            "running": self.running,
            "connected_systems": list(
                self.systems.keys()
            ),
            "missions": len(self.missions),
            "health": self.health(),
            "timestamp": time.time()
        }


genesis_control_plane = GenesisControlPlane()
