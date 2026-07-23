import time


class GenesisNetworkGraph:


    def __init__(self):

        self.connections = []


    def connect(
        self,
        source,
        relationship,
        target
    ):

        connection = {

            "source":
                source,

            "relationship":
                relationship,

            "target":
                target,

            "timestamp":
                time.time()

        }


        self.connections.append(connection)


        return connection


    def all(self):

        return self.connections
