import time


class GenesisDeliveryManager:


    def __init__(self):

        self.projects = []


    def create_project(
        self,
        client,
        service
    ):

        project = {

            "client":
                client,

            "service":
                service,

            "tasks":

                [

                "Build automation",

                "Test system",

                "Deploy solution"

                ],

            "status":
                "STARTED",

            "timestamp":
                time.time()

        }


        self.projects.append(project)


        return project
