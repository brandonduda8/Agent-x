from datetime import datetime


class GenesisAgent:

    def __init__(self,name,role):

        self.name=name
        self.role=role
        self.status="ONLINE"



    def report(self):

        return {

            "agent":self.name,

            "role":self.role,

            "status":self.status,

            "heartbeat":str(datetime.now())

        }



    def execute(self,mission):

        return {

            "agent":self.name,

            "mission":mission,

            "result":"EXECUTED",

            "time":str(datetime.now())

        }



if __name__=="__main__":

    agent=GenesisAgent(
        "Hermes Agent",
        "Communication Intelligence"
    )

    print(agent.report())
