import time
import uuid


class GenesisSalesConversationIntelligenceEngine:

    def __init__(self):
        self.analyses = []
        self.responses = []
        self.crm_updates = []


    def analyze_message(
        self,
        prospect,
        message
    ):

        text = message.lower()

        if any(word in text for word in [
            "price",
            "cost",
            "how much",
            "pricing"
        ]):
            intent = "PRICING_INTEREST"
            action = "SEND_OFFER"

        elif any(word in text for word in [
            "already use",
            "software",
            "system",
            "tool"
        ]):
            intent = "OBJECTION_EXISTING_SOLUTION"
            action = "EXPLAIN_ADVANTAGE"

        elif any(word in text for word in [
            "demo",
            "call",
            "meeting",
            "schedule"
        ]):
            intent = "READY_TO_BUY"
            action = "CREATE_SALES_CALL"

        else:
            intent = "GENERAL_INTEREST"
            action = "CONTINUE_CONVERSATION"


        analysis = {
            "id":
                f"conversation_analysis_{uuid.uuid4().hex[:8]}",
            "prospect":
                prospect.get("id"),
            "company":
                prospect.get("company"),
            "message":
                message,
            "intent":
                intent,
            "recommended_action":
                action,
            "timestamp":
                time.time()
        }

        self.analyses.append(
            analysis
        )

        return analysis


    def generate_response(
        self,
        analysis
    ):

        intent = analysis["intent"]

        if intent == "PRICING_INTEREST":

            response = (
                "Our AI automation package is "
                "designed around your workflow needs. "
                "I would like to understand your process "
                "and show you the best implementation."
            )

        elif intent == "OBJECTION_EXISTING_SOLUTION":

            response = (
                "That's great that you already have tools. "
                "Genesis focuses on connecting workflows "
                "and reducing manual steps your current tools "
                "may not cover."
            )

        elif intent == "READY_TO_BUY":

            response = (
                "Excellent. Let's schedule a quick discovery "
                "call and prepare a demo based on your workflow."
            )

        else:

            response = (
                "I would love to learn more about your current "
                "workflow and identify where AI automation can help."
            )


        result = {
            "id":
                f"response_{uuid.uuid4().hex[:8]}",
            "analysis":
                analysis["id"],
            "response":
                response,
            "status":
                "READY",
            "timestamp":
                time.time()
        }

        self.responses.append(
            result
        )

        return result


    def update_crm(
        self,
        prospect_id,
        stage
    ):

        update = {
            "id":
                f"crm_update_{uuid.uuid4().hex[:8]}",
            "prospect":
                prospect_id,
            "stage":
                stage,
            "timestamp":
                time.time()
        }

        self.crm_updates.append(
            update
        )

        return update


    def report(self):

        return {
            "system":
                "GENESIS SALES CONVERSATION INTELLIGENCE ENGINE v1",
            "analyses":
                len(self.analyses),
            "responses":
                len(self.responses),
            "crm_updates":
                len(self.crm_updates),
            "status":
                "ONLINE",
            "timestamp":
                time.time()
        }


genesis_sales_conversation_intelligence_engine = (
    GenesisSalesConversationIntelligenceEngine()
)
