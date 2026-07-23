import json


from core.genesis.genesis_omega_live_runtime import (
    genesis_omega_live_runtime
)


def main():


    runtime = genesis_omega_live_runtime


    runtime.register_component(
        "android_mcp"
    )

    runtime.register_component(
        "openhands"
    )

    runtime.register_component(
        "open_interpreter"
    )

    runtime.register_component(
        "mcp_adapter_fabric"
    )

    runtime.register_component(
        "ceo_runtime"
    )

    runtime.register_component(
        "business_loop"
    )

    runtime.register_component(
        "crm"
    )

    runtime.register_component(
        "revenue_engine"
    )


    print(
        json.dumps(
            runtime.boot(),
            indent=4
        )
    )


    print(
        json.dumps(
            runtime.health(),
            indent=4
        )
    )



if __name__ == "__main__":
    main()
