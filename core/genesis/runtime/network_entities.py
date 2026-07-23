import time
import uuid


class GenesisNetworkEntities:


    def __init__(self):

        self.entities = []


    def create(
        self,
        entity_type,
        name,
        data
    ):

        entity = {

            "id":
                entity_type + "_" +
                uuid.uuid4().hex[:8],

            "type":
                entity_type,

            "name":
                name,

            "data":
                data,

            "timestamp":
                time.time()

        }


        self.entities.append(entity)


        return entity


    def all(self):

        return self.entities
