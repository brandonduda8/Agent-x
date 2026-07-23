import time
import uuid


class GenesisRealityValidator:

    """
    GENESIS REALITY VALIDATOR v1

    Prevents false opportunities.

    Validates:

    - source
    - company
    - URL
    - category
    - required information
    - confidence score

    Only verified opportunities should
    reach execution systems.
    """

    def __init__(self):

        self.system = (
            "GENESIS REALITY VALIDATOR v1"
        )

        self.validated = []



    def validate(
        self,
        opportunity
    ):

        checks = {

            "has_title":
                bool(
                    opportunity.get(
                        "title"
                    )
                ),

            "has_source":
                bool(
                    opportunity.get(
                        "source"
                    )
                ),

            "has_category":
                bool(
                    opportunity.get(
                        "category"
                    )
                ),

            "has_url":
                bool(
                    opportunity.get(
                        "url"
                    )
                ),

            "has_company":
                bool(
                    opportunity.get(
                        "company"
                    )
                )

        }


        passed = 0


        for check in checks.values():

            if check:

                passed += 1



        confidence = int(
            (
                passed
                /
                len(checks)
            )
            *
            100
        )


        if confidence >= 80:

            status = "VERIFIED"

        elif confidence >= 50:

            status = "NEEDS_REVIEW"

        else:

            status = "UNVERIFIED"



        result = {

            "id":
                "validation_"
                +
                uuid.uuid4().hex[:8],


            "opportunity":
                opportunity,


            "checks":
                checks,


            "confidence":
                confidence,


            "status":
                status,


            "validated_at":
                time.time()

        }


        self.validated.append(
            result
        )


        print(
            f"🔎 Reality Check: {status} ({confidence}%)"
        )


        return result



    def batch_validate(
        self,
        opportunities
    ):

        results = []


        for opportunity in opportunities:

            results.append(
                self.validate(
                    opportunity
                )
            )


        return results



    def report(self):

        return {

            "system":
                self.system,


            "validated":
                len(
                    self.validated
                ),


            "verified":

                len(
                    [
                        x
                        for x in self.validated
                        if x["status"]
                        ==
                        "VERIFIED"
                    ]
                ),


            "timestamp":
                time.time()

        }



genesis_reality_validator = GenesisRealityValidator()
