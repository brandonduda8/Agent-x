import os
import json
import time
import uuid


class GenesisApplicationAgent:

    """
    GENESIS APPLICATION AGENT v1

    Turns matched jobs into
    organized application packages.
    """

    def __init__(self):

        self.system = (
            "GENESIS APPLICATION AGENT v1"
        )

        self.file = (
            "data/genesis_applications.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                        "applications": []
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



    def save(self,data):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def create_application(
        self,
        job,
        candidate_profile
    ):

        data = self.load()


        application = {

            "id":
                "application_"
                +
                uuid.uuid4().hex[:8],


            "job":
                job.get("title"),


            "company":
                job.get("company"),


            "status":
                "READY",


            "resume_focus":
                candidate_profile.get(
                    "skills",
                    []
                ),


            "cover_letter":

                f"""
Hello {job.get('company')},

I am interested in the {job.get('title')} position.

My experience includes:
{', '.join(candidate_profile.get('skills', []))}

I specialize in building AI automation,
Python systems, APIs, and intelligent workflows.

I would love the opportunity to contribute
to your team.

Thank you.
""",


            "created":
                time.time()

        }


        data["applications"].append(
            application
        )


        self.save(data)


        print(
            "📨 Application package created:"
        )

        print(
            application["job"]
        )


        return application



    def report(self):

        data = self.load()

        return {

            "system":
                self.system,

            "applications":
                len(
                    data["applications"]
                ),

            "timestamp":
                time.time()

        }



application_agent = GenesisApplicationAgent()
