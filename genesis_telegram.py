from genesis_core.config.env_loader import GenesisEnvironmentLoader
from genesis_core.telegram.telegram_connector import GenesisTelegramConnector


# Load Genesis secrets/configuration
env = GenesisEnvironmentLoader()
env.load()


state = {

    "systems":

    [
        "CEO Loop",
        "World Intelligence",
        "Agent Workforce",
        "OpenRouter",
        "Stripe",
        "Telegram"
    ],


    "opportunities":

    [
        "Dental AI Automation Client",
        "AI Data Specialist"
    ],


    "missions":

    [
        "Acquire Dental AI Client"
    ]

}


bot = GenesisTelegramConnector(
    state
)


bot.start()
