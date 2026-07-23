import time


class GenesisConnectorMigration:


    def __init__(
        self,
        adapter_manager,
        connector_registry
    ):

        self.adapter_manager = adapter_manager

        self.connector_registry = connector_registry

        self.system = (
            "GENESIS CONNECTOR MIGRATION v1"
        )



    def migrate(self):

        connected = (
            self.adapter_manager.connect_all()
        )


        return {

            "system":
                self.system,

            "migrated_adapters":
                connected,

            "connector_registry":
                self.connector_registry.discover(),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
