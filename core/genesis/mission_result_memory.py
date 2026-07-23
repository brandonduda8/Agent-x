import time
import uuid


class GenesisMissionResultMemory:

    """
    GENESIS MISSION RESULT MEMORY v1

    Stores agent execution outputs.

    Flow:

    Agent Result
        |
        v
    Result Memory
        |
        v
    Mission Outcome Engine
    """


    def __init__(self):

        self.system = (
            "GENESIS MISSION RESULT MEMORY v1"
        )

        self.results = []



    def store(
        self,
        event
    ):

        payload = event.get(
            "payload",
            {}
        )


        record = {

            "id":
                "result_"
                + uuid.uuid4().hex[:8],

            "agent":
                event.get(
                    "source"
                ),

            "mission_id":
                payload.get(
                    "mission_id"
                ),

            "capabilities":
                payload.get(
                    "capabilities",
                    []
                ),

            "result":
                payload.get(
                    "result",
                    payload
                ),

            "timestamp":
                time.time()

        }


        self.results.append(
            record
        )


        print(
            f"🧠 Result memory stored: {record['agent']}"
        )


        return record




    def get_mission_results(
        self,
        mission_id
    ):

        return [

            result

            for result in self.results

            if result.get(
                "mission_id"
            ) == mission_id

        ]



    def latest(self):

        if not self.results:

            return None


        return self.results[-1]



    def report(self):

        return {

            "system":
                self.system,

            "stored_results":
                len(
                    self.results
                ),

            "timestamp":
                time.time()

        }



mission_result_memory = (
    GenesisMissionResultMemory()
)
