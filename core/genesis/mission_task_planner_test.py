from core.genesis.mission_task_planner import (
    mission_task_planner
)


mission = {
    "id": "mission_demo"
}


team = {

    "team": [

        {
            "agent":
                "Coding Agent",

            "matched_skills":
                [
                    "coding",
                    "deployment"
                ]

        },

        {
            "agent":
                "Revenue Agent",

            "matched_skills":
                [
                    "sales",
                    "lead_generation"
                ]

        }

    ]

}


result = mission_task_planner.create_plan(
    mission,
    team
)


print(result)

print(
    mission_task_planner.report()
)
