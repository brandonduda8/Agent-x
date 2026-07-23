import time
import uuid


class GenesisAndroidTaskExecutor:


    def __init__(self):

        self.system = (
            "GENESIS ANDROID TASK EXECUTOR v1"
        )


    def prepare(
        self,
        task
    ):


        return {

            "id":
                "android_task_" +
                uuid.uuid4().hex[:8],

            "task":
                task,

            "status":
                "READY_FOR_APPROVAL",

            "timestamp":
                time.time()

        }
