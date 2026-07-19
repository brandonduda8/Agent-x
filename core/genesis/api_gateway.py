import time
import uuid

from core.genesis.mobile_api_server import mobile_api_server
from core.genesis.event_stream import event_stream
from core.genesis.approval_gateway import approval_gateway


class GenesisAPIGateway:

    def __init__(self):

        self.system = "GENESIS API GATEWAY v1"

        self.requests = []



    def command(
        self,
        command
    ):

        request = {

            "id":
            "request_" + uuid.uuid4().hex[:8],

            "type":
            "COMMAND",

            "command":
            command,

            "timestamp":
            time.time()

        }


        self.requests.append(request)


        mobile_api_server.receive_command(
            command,
            "api_gateway"
        )


        event_stream.emit(
            "COMMAND_RECEIVED",
            "API Gateway",
            {
                "command":
                command
            }
        )


        return request



    def agents(self):

        return mobile_api_server.get_agents()



    def missions(self):

        return mobile_api_server.get_missions()



    def approve(
        self,
        action
    ):

        result = approval_gateway.request_action(
            "Genesis User",
            "device_changes",
            action
        )

        return result



    def events(self):

        return event_stream.latest()



    def status(self):

        return {

            "system":
            self.system,

            "status":
            "ONLINE",

            "requests":
            len(self.requests),

            "timestamp":
            time.time()

        }



api_gateway = GenesisAPIGateway()
