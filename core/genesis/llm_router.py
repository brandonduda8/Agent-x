import time


class GenesisLLMRouter:

    def __init__(self):

        self.system = "GENESIS LLM ROUTER v1"

        self.providers = {}

        self.agent_models = {}



    def register_provider(
        self,
        name,
        model,
        provider
    ):

        self.providers[name] = {

            "model": model,

            "provider": provider,

            "status": "CONNECTED",

            "timestamp": time.time()

        }


        print(
            f"🧠 LLM connected: {name}"
        )


    def connect_agent(
        self,
        agent,
        provider
    ):

        if provider in self.providers:

            self.agent_models[agent] = provider


            print(
                f"🔗 {agent} connected to {provider}"
            )


            return True


        return False



    def route(
        self,
        agent,
        task
    ):

        provider = self.agent_models.get(agent)


        return {

            "agent": agent,

            "provider": provider,

            "task": task,

            "status": "READY",

            "timestamp": time.time()

        }



    def report(self):

        return {

            "system": self.system,

            "providers": self.providers,

            "agents": self.agent_models,

            "timestamp": time.time()

        }



llm_router = GenesisLLMRouter()
