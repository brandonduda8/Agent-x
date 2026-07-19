from core.genesis.control_plane import GenesisControlPlane
from core.genesis.genesis_kernel import genesis_kernel
from core.genesis.master_controller import genesis_controller
from core.genesis.tool_registry import tool_registry


def main():

    control = GenesisControlPlane(
        kernel=genesis_kernel,
        controller=genesis_controller,
        tools=tool_registry
    )

    control.register_system(
        "Genesis Kernel",
        genesis_kernel
    )

    control.register_system(
        "Master Controller",
        genesis_controller
    )

    control.register_system(
        "Tool Registry",
        tool_registry
    )

    control.start()

    mission = control.create_mission(
        "Find AI automation customers"
    )

    print(mission)

    print(control.discover_capabilities())

    print(control.report())


if __name__ == "__main__":
    main()
