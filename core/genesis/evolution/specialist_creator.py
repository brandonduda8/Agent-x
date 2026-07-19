import time
import uuid


class GenesisSpecialistCreator:


    def __init__(self):

        self.system = "GENESIS SPECIALIST CREATOR v1"
        self.specialists = []



    def create(
        self,
        agent,
        capability
    ):

        print(
            "🏗 Creating evolved specialist"
        )


        name = (
            capability
            .replace("_"," ")
            .title()
            +
            " Specialist"
        )


        specialist = {

            "id":
            "specialist_" +
            uuid.uuid4().hex[:8],

            "name": name,

            "origin_agent": agent,

            "skills":[
                capability
            ],

            "status":"CREATED",

            "timestamp":time.time()

        }


        self.specialists.append(
            specialist
        )


        print(
            f"🏗 Specialist created: {name}"
        )


        return specialist



    def report(self):

        return {

            "system":self.system,

            "specialists":len(self.specialists),

            "timestamp":time.time()

        }



specialist_creator = GenesisSpecialistCreator()
