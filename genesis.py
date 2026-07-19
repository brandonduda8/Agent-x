from core.genesis.master_controller import genesis_controller
from core.genesis.agent_x_bridge import agent_x_bridge
from core.genesis.memory_engine import memory_engine


def boot():

    print("""
🧬 ================================
   GENESIS ANDROID AI CORE v0.1
================================
""")


    print("🔍 Loading device identity...")

    print(
        genesis_controller.identity
    )


    print("\n🧰 Loading capabilities...")

    print(
        genesis_controller.discover_capabilities()
    )


    print("\n🤖 Connecting Agent-X...")

    result = agent_x_bridge.connect()

    print(result)


    print("\n🧠 Memory Status...")

    print(
        memory_engine.memory
    )


    print("""
================================
 GENESIS STATUS: ONLINE
================================
""")


if __name__ == "__main__":
    boot()
