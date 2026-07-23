import datetime


class MissionRouter:

    def __init__(self):

        self.routes = {

            "income":
            {
                "agent":"Opportunity Discovery Agent",
                "adapter":"Job Discovery Adapter",
                "approval":True
            },

            "revenue":
            {
                "agent":"Revenue Agent",
                "adapter":"Business Lead Adapter",
                "approval":True
            },

            "housing":
            {
                "agent":"Stability Agent",
                "adapter":"Housing Resource Adapter",
                "approval":False
            },

            "technology":
            {
                "agent":"Technology Agent",
                "adapter":"Development Adapter",
                "approval":True
            }

        }


    def dispatch(self, mission_type, objective):

        route = self.routes.get(mission_type)

        if not route:

            return {
                "status":"ERROR",
                "message":"No route found"
            }


        return {

            "mission": objective,

            "assigned_agent":
            route["agent"],

            "adapter":
            route["adapter"],

            "approval_required":
            route["approval"],

            "timestamp":
            str(datetime.datetime.now()),

            "status":
            "DISPATCHED"

        }



if __name__ == "__main__":

    router = MissionRouter()


    print(
        router.dispatch(
            "revenue",
            "Find and prepare next client opportunity"
        )
    )


    print(
        router.dispatch(
            "income",
            "Find highest probability job matches"
        )
    )
