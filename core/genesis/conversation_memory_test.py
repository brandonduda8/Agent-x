from core.genesis.conversation_memory import conversation_memory


print(
    conversation_memory.remember(
        "Genesis",
        "Build AI workstation",
        "Creating communication layer"
    )
)


print(
    conversation_memory.report()
)


print(
    conversation_memory.recent()
)
