import time


class GenesisKernel:

    """
    GENESIS KERNEL v1

    Central dependency connection layer.

    Connects all Genesis systems.
    """

    def __init__(self):

        self.system = "GENESIS KERNEL v1"

        self.components = {}

        self.boot_time = time.time()


    def register(self, name, component):

        self.components[name] = component

        print(
            f"🔗 Genesis connected: {name}"
        )


    def get(self, name):

        return self.components.get(name)


    def status(self):

        return {
            "system": self.system,
            "components": list(
                self.components.keys()
            ),
            "online": len(self.components),
            "timestamp": time.time()
        }


genesis_kernel = GenesisKernel()
