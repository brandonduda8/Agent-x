import time
import uuid
import json
import os


class GenesisSalesPartnerAgent:

    """
    GENESIS SALES PARTNER AGENT v1

    Finds and manages commission-based
    sales partners for Genesis opportunities.

    Purpose:

    Opportunity
          |
          v
    Sales Partner Matching
          |
          v
    Commission Agreement
          |
          v
    Deal Tracking
    """

    def __init__(self):

        self.system = (
            "GENESIS SALES PARTNER AGENT v1"
        )

        self.file = (
            "data/genesis_sales_partners.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(
            self.file
        ):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                        "partners": [],
                        "offers": [],
                        "matches": []
                    },
                    f,
                    indent=2
                )



    def load(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def add_partner(
        self,
        name,
        contact,
        skills,
        commission=50
    ):

        data = self.load()


        partner = {

            "id":
                "partner_"
                +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "contact":
                contact,

            "skills":
                skills,

            "commission_percent":
                commission,

            "status":
                "AVAILABLE",

            "created":
                time.time()

        }


        data["partners"].append(
            partner
        )


        self.save(
            data
        )


        print(
            f"🤝 Sales Partner Added: {name}"
        )


        return partner



    def create_commission_offer(
        self,
        opportunity,
        commission=50
    ):

        data = self.load()


        offer = {

            "id":
                "offer_"
                +
                uuid.uuid4().hex[:8],

            "opportunity":
                opportunity,

            "commission_percent":
                commission,

            "status":
                "OPEN",

            "created":
                time.time()

        }


        data["offers"].append(
            offer
        )


        self.save(
            data
        )


        print(
            "💰 Commission Offer Created"
        )


        return offer



    def match_partner(
        self,
        opportunity
    ):

        data = self.load()


        if not data["partners"]:

            return {

                "status":
                    "NO_PARTNERS_AVAILABLE",

                "message":
                    "Genesis needs sales partners"

            }


        partner = data["partners"][0]


        match = {

            "id":
                "match_"
                +
                uuid.uuid4().hex[:8],

            "partner":
                partner["id"],

            "opportunity":
                opportunity,

            "commission":
                partner["commission_percent"],

            "status":
                "MATCHED",

            "created":
                time.time()

        }


        data["matches"].append(
            match
        )


        self.save(
            data
        )


        return match



    def report(self):

        data = self.load()


        return {

            "system":
                self.system,

            "partners":
                len(
                    data["partners"]
                ),

            "offers":
                len(
                    data["offers"]
                ),

            "matches":
                len(
                    data["matches"]
                ),

            "timestamp":
                time.time()

        }



sales_partner_agent = GenesisSalesPartnerAgent()
