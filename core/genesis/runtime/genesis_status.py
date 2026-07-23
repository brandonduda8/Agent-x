import time


class GenesisStatusReporter:


    def report(
        self,
        dashboard
    ):


        return {


            "genesis":
                dashboard["system"],


            "health":
                dashboard["status"],


            "active_systems":
                len(
                    dashboard["systems"]
                ),


            "timestamp":
                time.time()

        }
