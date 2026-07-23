import time
import uuid


class GenesisAgentFactory:


    def __init__(self):

        self.blueprints = []



    def create_blueprint(
        self,
        capability,
        purpose
    ):

        blueprint = {

            "id":
            "blueprint_" +
            uuid.uuid4().hex[:8],

            "name":
            "Genesis " +
            capability.title() +
            " Agent",

            "capability":
            capability,

            "purpose":
            purpose,

            "role":
            self.generate_role(
                capability
            ),

            "system_prompt":
            self.generate_prompt(
                capability,
                purpose
            ),

            "tools":
            self.assign_tools(
                capability
            ),

            "model":
            self.assign_model(
                capability
            ),

            "status":
            "READY_FOR_DEPLOYMENT",

            "timestamp":
            time.time()

        }


        self.blueprints.append(
            blueprint
        )


        return blueprint



    def generate_role(
        self,
        capability
    ):

        roles = {

            "marketing":
            "Acquire customers and grow revenue",

            "research":
            "Discover and analyze intelligence",

            "coding":
            "Build and maintain software",

            "sales":
            "Convert opportunities into revenue"

        }


        return roles.get(

            capability,

            "Specialized Genesis Worker"

        )



    def generate_prompt(
        self,
        capability,
        purpose
    ):

        return (

            "You are a Genesis "

            + capability

            + " specialist. "

            "Your mission is: "

            + purpose

            + ". "

            "Work with the Genesis ecosystem."

        )



    def assign_tools(
        self,
        capability
    ):

        tool_map = {

            "marketing":

            [

            "research",

            "content",

            "analytics"

            ],


            "sales":

            [

            "CRM",

            "outreach",

            "tracking"

            ],


            "coding":

            [

            "repository",

            "testing",

            "deployment"

            ]

        }


        return tool_map.get(

            capability,

            [

            "reasoning",

            "memory"

            ]

        )



    def assign_model(
        self,
        capability
    ):

        return {

            "provider":
            "OpenRouter",

            "routing":
            capability,

            "tier":
            "FREE"

        }



    def status(self):

        return {

            "system":
            "GENESIS AGENT CREATION FACTORY v1",

            "blueprints":
            len(self.blueprints),

            "timestamp":
            time.time()

        }
