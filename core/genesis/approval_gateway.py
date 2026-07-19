import time
import uuid


class GenesisApprovalGateway:

    def __init__(self):

        self.system = "GENESIS APPROVAL GATEWAY v1"

        self.requests = []

        self.rules = {

            "create_content": "AUTO",

            "research": "AUTO",

            "analyze_revenue": "AUTO",

            "write_code": "AUTO",

            "send_messages": "APPROVAL",

            "create_payments": "APPROVAL",

            "deploy_system": "APPROVAL",

            "device_changes": "APPROVAL"

        }



    def request_action(
        self,
        agent,
        action,
        details=None
    ):

        permission = self.rules.get(
            action,
            "APPROVAL"
        )


        request = {

            "id":
            "approval_" + uuid.uuid4().hex[:8],

            "agent":
            agent,

            "action":
            action,

            "details":
            details,

            "permission":
            permission,

            "status":
            "APPROVED"
            if permission == "AUTO"
            else "WAITING_FOR_USER",

            "timestamp":
            time.time()

        }


        self.requests.append(request)


        return request



    def approve(
        self,
        request_id
    ):

        for request in self.requests:

            if request["id"] == request_id:

                request["status"] = "APPROVED"

                return request


        return None



    def deny(
        self,
        request_id
    ):

        for request in self.requests:

            if request["id"] == request_id:

                request["status"] = "DENIED"

                return request


        return None



    def report(self):

        return {

            "system":
            self.system,

            "requests":
            len(self.requests),

            "timestamp":
            time.time()

        }



approval_gateway = GenesisApprovalGateway()
