import os
import time


class GenesisAndroidStorageAdapter:


    def __init__(self):

        self.system = (
            "GENESIS ANDROID STORAGE ADAPTER v1"
        )


    def inspect(
        self,
        path="."
    ):


        return {

            "path":
                path,

            "exists":
                os.path.exists(path),

            "files":
                os.listdir(path)
                if os.path.exists(path)
                else [],

            "timestamp":
                time.time()

        }
