import time

from core.genesis.lead_database import lead_database
from core.genesis.memory_engine import memory_engine


class GenesisSalesAgent:

    def __init__(self):

        self.name = "GENESIS SALES AGENT v1"

        self.actions = []



    def analyze_lead(self, lead):

        status = lead.get(
            "status",
            "NEW"
        )


        if status == "NEW":

            action = "SEND_INTRO_MESSAGE"

            message = (
                f"Hello {lead['contact']}, "
                f"we help {lead['industry']} companies "
                "automate customer workflows with AI. "
                "Would you like to see how it works?"
            )


        elif status == "CONTACTED":

            action = "FOLLOW_UP"

            message = (
                "Following up to see if improving "
                "your workflow automation is a priority."
            )


        elif status == "REPLIED":

            action = "BOOK_DEMO"

            message = (
                "Great! Let's schedule a quick demo "
                "and show how the system can help."
            )


        else:

            action = "NURTURE"

            message = (
                "Continue relationship building."
            )


        result = {

            "lead":
                lead["id"],

            "action":
                action,

            "message":
                message,

            "timestamp":
                time.time()

        }


        self.actions.append(
            result
        )


        memory_engine.remember_knowledge(
            "sales_action",
            result,
            confidence=0.8
        )


        return result



    def process_all_leads(self):

        results = []

        for lead in lead_database.get_leads():

            results.append(
                self.analyze_lead(lead)
            )


        return results



    def report(self):

        return {

            "engine":
                self.name,

            "actions":
                len(self.actions),

            "timestamp":
                time.time()

        }



sales_agent = GenesisSalesAgent()
