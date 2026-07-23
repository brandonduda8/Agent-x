import time
import uuid


class GenesisSourceAdapterLayer:

    """
    GENESIS SOURCE ADAPTER LAYER v1

    Converts external sources into Genesis opportunities.
    """

    def __init__(self):

        self.system = (
            "GENESIS SOURCE ADAPTER LAYER v1"
        )

        self.adapters = {}

        self.sync_history = []



    def register_adapter(
        self,
        name,
        category,
        function
    ):

        adapter = {

            "id":
                "adapter_"
                +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "category":
                category,

            "function":
                function,

            "status":
                "ACTIVE",

            "created":
                time.time()

        }


        self.adapters[name] = adapter


        print(
            f"🔌 Adapter online: {name}"
        )


        return adapter



    def sync(
        self,
        name
    ):

        if name not in self.adapters:

            return {
                "status":
                "NOT_FOUND"
            }


        adapter = self.adapters[name]


        opportunities = (
            adapter["function"]()
        )


        event = {

            "id":
                "sync_"
                +
                uuid.uuid4().hex[:8],

            "adapter":
                name,

            "found":
                len(opportunities),

            "timestamp":
                time.time()

        }


        self.sync_history.append(
            event
        )


        return {

            "adapter":
                name,

            "opportunities":
                opportunities,

            "event":
                event

        }



    def report(self):

        return {

            "system":
                self.system,

            "adapters":
                len(
                    self.adapters
                ),

            "syncs":
                len(
                    self.sync_history
                ),

            "timestamp":
                time.time()

        }



genesis_source_adapter_layer = GenesisSourceAdapterLayer()
