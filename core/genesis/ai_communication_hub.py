import time


class GenesisAICommunicationHub:

    def __init__(self):

        self.system = "GENESIS AI COMMUNICATION HUB v1"

        self.providers = {}

        self.messages = []


    def register_provider(self, name, provider):

        self.providers[name] = provider

        print(f"🧠 AI Provider connected: {name}")

        return {
            "provider": name,
            "status": "CONNECTED"
        }


    async def send(self, provider, message):

        record = {

            "provider": provider,

            "message": message,

            "timestamp": time.time()

        }

        self.messages.append(record)


        print(
            f"📡 Sending to {provider}: {message}"
        )


        if provider in self.providers:

            ai = self.providers[provider]

            if hasattr(ai, "chat"):

                return await ai.chat(message)


        return {

            "status": "QUEUED",

            "provider": provider,

            "message": message

        }


    def broadcast(self, message):

        results = []

        for provider in self.providers:

            results.append(
                {
                    "provider": provider,
                    "message": message
                }
            )

        return results



    def report(self):

        return {

            "system": self.system,

            "providers": list(self.providers.keys()),

            "messages": len(self.messages),

            "timestamp": time.time()

        }


ai_hub = GenesisAICommunicationHub()
