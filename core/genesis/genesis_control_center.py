import time


class GenesisControlCenter:


    def __init__(self):

        self.system = (
            "GENESIS OMEGA CONTROL CENTER v1"
        )

        self.components = {}



    def connect(
        self,
        name,
        component
    ):

        self.components[name] = component

        return {
            "connected": name,
            "timestamp": time.time()
        }



    def collect(self):

        dashboard = {

            "system":
                self.system,

            "status":
                "ONLINE",

            "components": {},

            "timestamp":
                time.time()

        }


        for name, component in self.components.items():

            try:

                if hasattr(component, "report"):

                    dashboard["components"][name] = (
                        component.report()
                    )

                elif hasattr(component, "dashboard"):

                    dashboard["components"][name] = (
                        component.dashboard()
                    )

                else:

                    dashboard["components"][name] = {
                        "status":
                        "CONNECTED"
                    }


            except Exception as e:

                dashboard["components"][name] = {
                    "error":
                    str(e)
                }


        return dashboard



genesis_control_center = GenesisControlCenter()
