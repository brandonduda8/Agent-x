import time


class GenesisAndroidAdapter:


    def __init__(
        self,
        device,
        storage,
        executor
    ):

        self.device = device
        self.storage = storage
        self.executor = executor

        self.system = (
            "GENESIS ANDROID INTEGRATION ADAPTER v1"
        )


    def health_check(self):

        return {

            "system":
                self.system,

            "device":
                self.device.status(),

            "storage":
                self.storage.inspect(),

            "status":
                "CONNECTED",

            "timestamp":
                time.time()

        }


    def request_task(
        self,
        task
    ):

        return self.executor.prepare(
            task
        )
