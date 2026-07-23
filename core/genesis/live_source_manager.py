import time
import uuid
import json
import os


class GenesisLiveSourceManager:

    """
    GENESIS LIVE SOURCE MANAGER v2

    Manages real external opportunity sources.

    Tracks:

    - job feeds
    - freelance feeds
    - company sources
    - API connectors
    - sync history
    """

    def __init__(self):

        self.system = (
            "GENESIS LIVE SOURCE MANAGER v2"
        )

        self.file = (
            "data/genesis_live_sources.json"
        )

        self.sources = []

        self.sync_history = []

        os.makedirs(
            "data",
            exist_ok=True
        )

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

                    data = json.load(f)

                    self.sources = data.get(
                        "sources",
                        []
                    )

                    self.sync_history = data.get(
                        "syncs",
                        []
                    )

            except Exception:

                pass



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                {
                    "sources":
                        self.sources,

                    "syncs":
                        self.sync_history
                },
                f,
                indent=2
            )



    def register_source(
        self,
        name,
        category,
        connector,
        url=None
    ):

        source = {

            "id":
                "source_"
                +
                uuid.uuid4().hex[:8],


            "name":
                name,


            "category":
                category,


            "connector":
                connector,


            "url":
                url,


            "status":
                "ACTIVE",


            "created":
                time.time()

        }


        self.sources.append(
            source
        )

        self.save()


        print(
            f"🌐 Source Connected: {name}"
        )


        return source



    def list_sources(self):

        return self.sources



    def record_sync(
        self,
        source,
        found
    ):

        sync = {

            "id":
                "sync_"
                +
                uuid.uuid4().hex[:8],


            "source":
                source,


            "opportunities_found":
                found,


            "timestamp":
                time.time()

        }


        self.sync_history.append(
            sync
        )

        self.save()


        return sync



    def report(self):

        return {

            "system":
                self.system,


            "sources":
                len(
                    self.sources
                ),


            "syncs":
                len(
                    self.sync_history
                ),


            "timestamp":
                time.time()

        }



genesis_live_source_manager = GenesisLiveSourceManager()
