import time
import uuid


class GenesisAutonomousSalesAgent:

    def __init__(self):
        self.sales_actions = []
        self.conversations = []
        self.outcomes = []


    def create_sales_action(
        self,
        prospect,
        intelligence
    ):

        priority = intelligence.get(
            "priority",
            "COLD"
        )

        if priority == "HOT":

            actions = [
                "Send personalized introduction",
                "Offer automation demo",
                "Request discovery call"
            ]

        elif priority == "WARM":

            actions = [
                "Send value message",
                "Share automation example",
                "Schedule follow-up"
            ]

        else:

            actions = [
                "Add to nurture campaign",
                "Collect more information"
            ]


        action = {
            "id":
                f"sales_action_{uuid.uuid4().hex[:8]}",
            "prospect":
                prospect.get("id"),
            "company":
                prospect.get("company"),
            "priority":
                priority,
            "actions":
                actions,
            "status":
                "READY",
            "timestamp":
                time.time()
        }


        self.sales_actions.append(
            action
        )

        return action


    def generate_message(
        self,
        prospect,
        offer
    ):

        message = f"""
Hello {prospect.get('company')},

I noticed your team may benefit from
AI automation around {prospect.get('problem')}.

Our AI systems help businesses reduce
manual work, improve response times,
and create more efficient workflows.

I would like to show you a quick demo
of how this could work for your organization.

Would you be open to a short conversation?

Thanks.
"""


        conversation = {
            "id":
                f"conversation_{uuid.uuid4().hex[:8]}",
            "prospect":
                prospect.get("id"),
            "offer":
                offer,
            "message":
                message.strip(),
            "status":
                "GENERATED",
            "timestamp":
                time.time()
        }


        self.conversations.append(
            conversation
        )

        return conversation


    def record_outcome(
        self,
        conversation_id,
        outcome
    ):

        result = {
            "id":
                f"outcome_{uuid.uuid4().hex[:8]}",
            "conversation":
                conversation_id,
            "outcome":
                outcome,
            "timestamp":
                time.time()
        }


        self.outcomes.append(
            result
        )

        return result


    def report(self):

        return {
            "system":
                "GENESIS AUTONOMOUS SALES AGENT v1",
            "sales_actions":
                len(self.sales_actions),
            "messages":
                len(self.conversations),
            "outcomes":
                len(self.outcomes),
            "status":
                "ONLINE",
            "timestamp":
                time.time()
        }


genesis_autonomous_sales_agent = GenesisAutonomousSalesAgent()
