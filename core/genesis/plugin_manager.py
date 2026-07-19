import importlib
import time


class GenesisPluginManager:

    def __init__(self):

        self.system = "GENESIS PLUGIN MANAGER v1"

        self.plugins = {}

        self.history = []


    def load(self, name, module_path, object_name):

        try:

            module = importlib.import_module(module_path)

            plugin = getattr(module, object_name)

            self.plugins[name] = plugin


            record = {
                "plugin": name,
                "status": "LOADED",
                "timestamp": time.time()
            }

            self.history.append(record)


            print(f"🔌 Plugin loaded: {name}")


            return record


        except Exception as e:

            error = {
                "plugin": name,
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.time()
            }

            self.history.append(error)


            print(f"❌ Plugin failed: {name}")

            return error



    def get(self, name):

        return self.plugins.get(name)



    def report(self):

        return {
            "system": self.system,
            "plugins_loaded": len(self.plugins),
            "plugins": list(self.plugins.keys()),
            "history": self.history,
            "timestamp": time.time()
        }



plugin_manager = GenesisPluginManager()
