import time
import uuid


class GenesisApprovalGateway:


    def __init__(self):

        self.requests = []

        self.system = (
            "GENESIS APPROVAL GATEWAY v1"
        )


    def request(
        self,
        action,
        target
    ):

        approval = {

            "id":
                "approval_" +
                uuid.uuid4().hex[:8],

            "action":
                action,

            "target":
                target,

            "status":
                "WAITING_APPROVAL",

            "timestamp":
                time.time()

        }


        self.requests.append(
            approval
        )

        return approval
