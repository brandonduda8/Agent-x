import time


class GenesisCommunicationQueue:


    def __init__(self):

        self.messages = []

        self.system = (
            "GENESIS COMMUNICATION QUEUE v1"
        )


    def create(
        self,
        business,
        message
    ):


        item = {

            "business":
                business,

            "message":
                message,

            "status":
                "QUEUED",

            "timestamp":
                time.time()

        }


        self.messages.append(item)

        return item
