import time
import uuid


class GenesisSalesCloserNetwork:

    """
    GENESIS SALES CLOSER NETWORK v1

    Finds and manages commission-based closers.
    """

    def __init__(self):

        self.system = (
            "GENESIS SALES CLOSER NETWORK v1"
        )

        self.closers = []
        self.matches = []


    def add_closer(
        self,
        name,
        skills,
        experience
    ):

        closer = {

            "id":
            "closer_" +
            uuid.uuid4().hex[:8],

            "name":
            name,

            "skills":
            skills,

            "experience":
            experience,

            "status":
            "AVAILABLE",

            "created":
            time.time()

        }


        self.closers.append(
            closer
        )

        return closer



    def match_deal(
        self,
        opportunity
    ):

        matches = []


        for closer in self.closers:

            score = 0


            if "sales" in [
                x.lower()
                for x in closer["skills"]
            ]:

                score += 50


            if (
                "ai" in
                str(opportunity).lower()
            ):

                score += 25


            if (
                closer["status"]
                ==
                "AVAILABLE"
            ):

                score += 25


            matches.append({

                "closer":
                closer,

                "deal":
                opportunity,

                "score":
                score,

                "commission":
                "50%",

                "status":
                "OFFERED"

            })


        self.matches.extend(
            matches
        )


        return matches



    def report(self):

        return {

            "system":
            self.system,

            "closers":
            len(self.closers),

            "matches":
            len(self.matches),

            "timestamp":
            time.time()

        }



sales_closer_network = GenesisSalesCloserNetwork()
