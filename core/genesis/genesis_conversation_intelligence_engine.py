import time
import uuid
import json
import os


class GenesisConversationIntelligenceEngine:


    def __init__(self):

        self.system = "GENESIS CONVERSATION INTELLIGENCE ENGINE v1"
        self.file = "data/genesis_conversation_memory.json"
        self.responses = []

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file,"r") as f:
                    self.responses = json.load(f).get(
                        "responses",
                        []
                    )

            except:

                self.responses = []


    def save(self):

        with open(self.file,"w") as f:

            json.dump(
                {
                    "system":self.system,
                    "responses":self.responses,
                    "updated":time.time()
                },
                f,
                indent=2
            )


    def analyze_response(self, company, message):

        text = message.lower()


        if any(word in text for word in [
            "interested",
            "tell me more",
            "sounds good",
            "let's talk"
        ]):

            intent = "INTERESTED"
            next_action = "BOOK_DISCOVERY_CALL"
            probability = 75


        elif any(word in text for word in [
            "price",
            "cost",
            "expensive",
            "how much"
        ]):

            intent = "PRICE_OBJECTION"
            next_action = "SEND_VALUE_BREAKDOWN"
            probability = 60


        elif any(word in text for word in [
            "not interested",
            "no thanks",
            "already have"
        ]):

            intent = "NOT_INTERESTED"
            next_action = "ADD_TO_NURTURE"
            probability = 20


        else:

            intent = "UNKNOWN"
            next_action = "FOLLOW_UP"
            probability = 40



        response = {

            "id":
                "conversation_"
                + uuid.uuid4().hex[:8],

            "company":
                company,

            "message":
                message,

            "analysis":{

                "intent":
                    intent,

                "next_action":
                    next_action,

                "probability":
                    probability

            },

            "created":
                time.time()

        }


        self.responses.append(
            response
        )

        self.save()


        print(
            f"🧠 Conversation Analyzed: {company} -> {intent}"
        )


        return response



    def report(self):

        return {

            "system":
                self.system,

            "responses":
                len(self.responses),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_conversation_intelligence_engine = (
    GenesisConversationIntelligenceEngine()
)
