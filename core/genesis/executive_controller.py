import time


class GenesisExecutiveController:

    def __init__(self):

        self.system = "GENESIS EXECUTIVE CONTROLLER v1"
        self.running = False
        self.cycles = 0
        self.events = []

        self.components = {}

    def register(self, name, component):

        self.components[name] = component

        self.events.append({
            "event": "SYSTEM_REGISTERED",
            "system": name,
            "timestamp": time.time()
        })

        print(f"🔗 Executive connected: {name}")


    def boot(self):

        print("=" * 50)
        print("👑 GENESIS EXECUTIVE CONTROLLER ONLINE")
        print("=" * 50)

        self.running = True

        self.events.append({
            "event": "EXECUTIVE_STARTED",
            "timestamp": time.time()
        })

        return self.status()


    def execute_cycle(self, objective):

        if not self.running:
            self.boot()

        self.cycles += 1

        print(f"👑 CEO Objective: {objective}")

        event = {

            "id": f"executive_cycle_{self.cycles}",

            "objective": objective,

            "systems": list(self.components.keys()),

            "status": "EXECUTING",

            "timestamp": time.time()

        }

        self.events.append(event)

        return event


    def status(self):

        return {

            "system": self.system,

            "running": self.running,

            "cycles": self.cycles,

            "connected_systems": list(self.components.keys()),

            "events": len(self.events),

            "timestamp": time.time()

        }


executive_controller = GenesisExecutiveController()
