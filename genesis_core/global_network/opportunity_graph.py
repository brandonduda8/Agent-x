import time


class GenesisOpportunityGraph:


    def build(
        self,
        opportunities
    ):

        nodes = []

        connections = []


        for opp in opportunities:

            node = {

                "id":
                opp["id"],

                "name":
                opp["name"],

                "type":
                opp["category"]

            }

            nodes.append(node)


            connections.append({

                "source":
                opp["id"],

                "relationship":
                "economic_opportunity",

                "timestamp":
                time.time()

            })


        return {

            "nodes":
            nodes,

            "connections":
            connections

        }
