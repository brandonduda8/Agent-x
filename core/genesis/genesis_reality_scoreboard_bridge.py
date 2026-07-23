import time

from core.genesis.genesis_result_harvester import result_harvester


class GenesisRealityScoreboard:

    def status(self):

        results = result_harvester.results

        return {
            "system": "GENESIS REALITY SCOREBOARD v2",
            "status": "ONLINE",

            "score": {

                "income": {
                    "jobs_found": len(results["income"]),
                    "applications": 0,
                    "interviews": 0,
                    "money_generated": 0
                },

                "revenue": {
                    "leads": len(results["revenue"]),
                    "offers": 0,
                    "clients": 0
                },

                "housing": {
                    "resources_found": len(results["housing"]),
                    "applications": 0,
                    "contacts": 0
                },

                "execution": {
                    "actions_completed": len(results["execution"])
                }

            },

            "timestamp": time.time()
        }


scoreboard = GenesisRealityScoreboard()
