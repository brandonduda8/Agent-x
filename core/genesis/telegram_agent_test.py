from core.genesis.telegram_agent import telegram_agent


print(
    telegram_agent.listen_once()
)


print(
    telegram_agent.report()
)
