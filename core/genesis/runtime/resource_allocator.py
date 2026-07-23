import time


class GenesisResourceAllocator:


    def allocate(
        self,
        ranked
    ):


        if not ranked:

            return {

                "decision":
                    "NO_ACTIVE_VENTURES"

            }


        top = max(

            ranked,

            key=lambda x:
                x["score"]

        )


        return {

            "priority_venture":
                top["venture"],

            "recommendation":

                "Increase resources",

            "timestamp":
                time.time()

        }
