import json


from core.genesis.genesis_omega_mission_commander import (
    genesis_omega_mission_commander
)


def main():

    commander = (
        genesis_omega_mission_commander
    )


    mission = commander.create_mission(
        "Acquire first AI automation customer",
        2500
    )


    print(
        json.dumps(
            mission,
            indent=4
        )
    )


    print(
        json.dumps(
            commander.assign_agents(
                mission["id"],
                [
                    "Genesis AI Engineer Agent",
                    "Genesis Software Engineer Agent",
                    "Genesis QA Scientist Agent"
                ]
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            commander.add_actions(
                mission["id"],
                [
                    "Build AI intake demo",
                    "Create sales presentation",
                    "Launch outreach campaign"
                ]
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            commander.record_revenue(
                mission["id"],
                2500
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            commander.complete(
                mission["id"],
                "AI automation package validated"
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            commander.report(),
            indent=4
        )
    )


if __name__ == "__main__":
    main()
