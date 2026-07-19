import time


class GenesisLLMRouterV2:

    def __init__(self):

        self.system = "GENESIS LLM ROUTER v2"

        self.providers = {}

        self.agents = {}


    def register_provider(
        self,
        name,
        model,
        capabilities
    ):

        self.providers[name] = {

            "model": model,

            "capabilities": capabilities,

            "status": "CONNECTED",

            "timestamp": time.time()

        }


        print(
            f"🧠 LLM provider connected: {name}"
        )


    def connect_agent(
        self,
        agent,
        provider
    ):

        self.agents[agent] = provider


        print(
            f"🔗 {agent} connected to {provider}"
        )


    def route_task(
        self,
        agent,
        task
    ):

        provider = self.agents.get(
            agent,
            "NONE"
        )


        return {

            "agent": agent,

            "task": task,

            "provider": provider,

            "status": "ROUTED",

            "timestamp": time.time()

        }



    def status(self):

        return {

            "system": self.system,

            "providers": self.providers,

            "agents": self.agents,

            "timestamp": time.time()

        }



llm_router_v2 = GenesisLLMRouterV2()
