import os
import json
import time
import uuid


class GenesisPersistentConnectorRegistry:

    """
    GENESIS PERSISTENT CONNECTOR REGISTRY v1

    Stores Genesis external opportunity sources.

    Purpose:

    - remember connectors after reboot
    - manage source inventory
    - prepare for API/feed adapters
    - support autonomous discovery
    """

    def __init__(self):

        self.system = (
            "GENESIS PERSISTENT CONNECTOR REGISTRY v1"
        )

        self.file = (
            "data/genesis_connectors.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.connectors = []

        self.load()



    def load(self):

        if os.path.exists(
            self.file
        ):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.connectors = json.load(f)

            except Exception:

                self.connectors = []



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.connectors,
                f,
                indent=2
            )



    def register(
        self,
        name,
        category,
        connector_type,
        url=None
    ):

        connector = {

            "id":
                "source_"
                +
                uuid.uuid4().hex[:8],


            "name":
                name,


            "category":
                category,


            "type":
                connector_type,


            "url":
                url,


            "status":
                "ACTIVE",


            "created":
                time.time()

        }


        self.connectors.append(
            connector
        )


        self.save()


        print(
            f"🌐 Persistent source registered: {name}"
        )


        return connector



    def list_sources(self):

        return self.connectors



    def report(self):

        return {

            "system":
                self.system,


            "sources":
                len(
                    self.connectors
                ),


            "timestamp":
                time.time()

        }



genesis_persistent_connector_registry = GenesisPersistentConnectorRegistry()
