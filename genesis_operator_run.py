import json


from core.genesis.genesis_omega_autonomous_operator import (
    genesis_omega_autonomous_operator
)


def main():

    operator = (
        genesis_omega_autonomous_operator
    )


    operation = (
        operator.start_operation(
            "Local law firm AI client intake automation",
            "HIGH"
        )
    )


    print(
        json.dumps(
            operation,
            indent=4
        )
    )


    print(
        json.dumps(
            operator.approve(
                operation["id"]
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            operator.assign_agents(
                operation["id"],
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
            operator.create_actions(
                operation["id"],
                [
                    "Build AI intake demo",
                    "Prepare client presentation",
                    "Generate outreach assets"
                ]
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            operator.complete(
                operation["id"],
                "Legal automation workflow optimized"
            ),
            indent=4
        )
    )


    print(
        json.dumps(
            operator.report(),
            indent=4
        )
    )



if __name__ == "__main__":
    main()
