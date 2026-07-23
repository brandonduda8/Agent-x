import time

from genesis_core.prime.genesis_prime import GenesisPrime
from genesis_core.opportunities.opportunity_scanner import GenesisOpportunityScanner
from genesis_core.missions.mission_engine import GenesisMissionEngine


class GenesisCommandRouter:


    def __init__(self):

        self.prime = GenesisPrime()

        self.scanner = GenesisOpportunityScanner()

        self.missions = GenesisMissionEngine()


        self.commands = {

            "/status": self.status,
            "/prime": self.prime_brief,
            "/jobs": self.jobs,
            "/business": self.business,
            "/missions": self.mission_status,
            "/help": self.help

        }



    def route(self, command):

        handler = self.commands.get(command)

        if handler:

            return handler()


        return {
            "message":
            "Unknown command. Use /help"
        }



    def status(self):

        return {

            "system":
            "GENESIS OS",

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



    def prime_brief(self):

        plan = self.prime.create_priority_plan()

        opportunities = self.scanner.scan()


        return {

            "system":
            "GENESIS PRIME DAILY BRIEF",


            "mission":
            plan["mission"],


            "top_priority":
            opportunities["opportunities"][0],


            "focus":

            [

                "Complete highest value task",

                "Move income pipeline forward",

                "Improve Genesis"

            ]

        }



    def jobs(self):

        opportunities = self.scanner.scan()


        return {

            "job_opportunities":

            [

                x for x in opportunities["opportunities"]

                if x["type"] == "REMOTE_WORK"

            ]

        }



    def business(self):

        opportunities = self.scanner.scan()


        return {

            "business_opportunities":

            [

                x for x in opportunities["opportunities"]

                if x["type"] != "REMOTE_WORK"

            ]

        }



    def mission_status(self):

        return self.missions.status()



    def help(self):

        return {

            "commands":

            list(self.commands.keys())

        }
