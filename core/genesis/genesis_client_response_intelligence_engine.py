import time
import json
import os
import uuid


class GenesisClientResponseIntelligenceEngine:

    def __init__(self):

        self.system = (
            "GENESIS CLIENT RESPONSE INTELLIGENCE ENGINE v1"
        )

        self.deals_file = (
            "data/genesis_deals.json"
        )

        self.responses_file = (
            "data/genesis_client_responses.json"
        )

        self.memory_file = (
            "data/genesis_sales_memory.json"
        )

        self.responses = []
        self.memory = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(
            self.responses_file
        ):
            try:
                with open(
                    self.responses_file,
                    "r"
                ) as f:
                    self.responses = json.load(f).get(
                        "responses",
                        []
                    )
            except Exception:
                self.responses = []


        if os.path.exists(
            self.memory_file
        ):
            try:
                with open(
                    self.memory_file,
                    "r"
                ) as f:
                    self.memory = json.load(f).get(
                        "memory",
                        []
                    )
            except Exception:
                self.memory = []



    def save(self):

        with open(
            self.responses_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system": self.system,
                    "responses": self.responses,
                    "updated": time.time()
                },
                f,
                indent=2
            )


        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system": self.system,
                    "memory": self.memory,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def classify_response(
        self,
        message
    ):

        text = message.lower()


        if any(
            word in text
            for word in [
                "interested",
                "tell me more",
                "sounds good",
                "yes"
            ]
        ):

            return {
                "intent": "INTERESTED",
                "next_action": "BOOK_DISCOVERY_CALL",
                "stage": "REPLIED",
                "probability": 50
            }


        if any(
            word in text
            for word in [
                "price",
                "expensive",
                "cost",
                "budget"
            ]
        ):

            return {
                "intent": "PRICE_OBJECTION",
                "next_action": "SEND_VALUE_BREAKDOWN",
                "stage": "NEGOTIATION",
                "probability": 60
            }


        if any(
            word in text
            for word in [
                "no",
                "not interested",
                "stop"
            ]
        ):

            return {
                "intent": "NOT_INTERESTED",
                "next_action": "STORE_LEARNING",
                "stage": "LOST",
                "probability": 0
            }


        return {
            "intent": "UNKNOWN",
            "next_action": "HUMAN_REVIEW",
            "stage": "CONTACTED",
            "probability": 20
        }



    def process_response(
        self,
        company,
        message
    ):

        analysis = self.classify_response(
            message
        )


        response = {

            "id":
                "response_"
                +
                uuid.uuid4().hex[:8],

            "company":
                company,

            "message":
                message,

            "analysis":
                analysis,

            "created":
                time.time()

        }


        self.responses.append(
            response
        )


        self.memory.append(

            {
                "company":
                    company,

                "lesson":
                    analysis["intent"],

                "action":
                    analysis["next_action"],

                "created":
                    time.time()
            }

        )


        self.save()


        print(
            "🧠 Response Analyzed:",
            company,
            "->",
            analysis["intent"]
        )


        return response



    def run_demo(self):

        examples = [

            (
                "Dental Service Company",
                "I am interested, tell me more"
            ),

            (
                "Dental Local Business",
                "How much does this cost?"
            )

        ]


        results = []


        for company, message in examples:

            results.append(
                self.process_response(
                    company,
                    message
                )
            )


        return {

            "system": self.system,

            "processed":
                len(results),

            "responses":
                results,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()
        }



    def report(self):

        return {

            "system":
                self.system,

            "responses":
                len(self.responses),

            "memory_entries":
                len(self.memory),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_client_response_intelligence_engine = (
    GenesisClientResponseIntelligenceEngine()
)
