import json
import datetime
import os


APPROVAL_FILE = "approvals.json"


class ApprovalEngine:

    def __init__(self):
        self.data = self.load()


    def load(self):

        if os.path.exists(APPROVAL_FILE):

            with open(APPROVAL_FILE, "r") as f:
                return json.load(f)

        return {
            "requests": []
        }


    def save(self):

        with open(APPROVAL_FILE, "w") as f:
            json.dump(self.data, f, indent=4)


    def create_request(self, agent, action, impact):

        request = {

            "id":
            len(self.data["requests"]) + 1,

            "agent":
            agent,

            "action":
            action,

            "impact":
            impact,

            "status":
            "WAITING",

            "created":
            str(datetime.datetime.now())

        }


        self.data["requests"].append(request)

        self.save()

        return request



    def approve(self, request_id):

        for request in self.data["requests"]:

            if request["id"] == request_id:

                request["status"] = "APPROVED"

                self.save()

                return request


        return {
            "error":
            "Request not found"
        }



    def deny(self, request_id):

        for request in self.data["requests"]:

            if request["id"] == request_id:

                request["status"] = "DENIED"

                self.save()

                return request


        return {
            "error":
            "Request not found"
        }




if __name__ == "__main__":


    engine = ApprovalEngine()


    request = engine.create_request(

        "Revenue Agent",

        "Contact potential business client",

        "Possible new revenue opportunity"

    )


    print(request)


    print(
        engine.approve(
            request["id"]
        )
    )
