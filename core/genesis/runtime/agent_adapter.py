import time


class GenesisAgentAdapter:


    def __init__(
        self,
        existing_agent,
        name=None,
        capabilities=None
    ):

        self.existing_agent = existing_agent

        self.name = (
            name
            or
            getattr(
                existing_agent,
                "name",
                existing_agent.__class__.__name__
            )
        )


        self.capabilities = (
            capabilities
            or
            getattr(
                existing_agent,
                "capabilities",
                []
            )
        )


        self.status = "CONNECTED"



    def execute(
        self,
        mission
    ):

        if hasattr(
            self.existing_agent,
            "execute"
        ):

            return self.existing_agent.execute(
                mission
            )


        if hasattr(
            self.existing_agent,
            "run"
        ):

            return self.existing_agent.run(
                mission
            )


        return {

            "agent":
                self.name,

            "mission":
                mission,

            "status":
                "NO_EXECUTION_METHOD"

        }



    def report(self):

        return {

            "agent":
                self.name,

            "capabilities":
                self.capabilities,

            "status":
                self.status,

            "timestamp":
                time.time()

        }
