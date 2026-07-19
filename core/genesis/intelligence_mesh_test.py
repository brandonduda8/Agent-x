from core.genesis.intelligence_mesh import GenesisIntelligenceMesh
from core.genesis.agent_registry import agent_registry
from core.genesis.agent_manager import agent_manager
from core.genesis.event_stream import event_stream
from core.genesis.tool_registry import tool_registry
from core.genesis.genesis_kernel import genesis_kernel


def main():

    agent_registry.register(
        "Agent-X",
        "Software Engineer",
        [
            "coding",
            "automation",
            "flutter"
        ]
    )

    agent_manager.register(
        "Agent-X",
        [
            "coding",
            "automation"
        ]
    )


    tool_registry.register_tool(
        "Genesis API",
        "integration",
        "Connect Genesis services",
        [
            "Agent-X"
        ]
    )


    mesh = GenesisIntelligenceMesh(
        agent_registry=agent_registry,
        agent_manager=agent_manager,
        event_stream=event_stream,
        tool_registry=tool_registry,
        kernel=genesis_kernel
    )


    mesh.start()


    print(
        mesh.assign_task(
            "Find and qualify AI automation customers"
        )
    )


    print(
        mesh.report()
    )


if __name__ == "__main__":
    main()
