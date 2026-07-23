from dotenv import load_dotenv
import os


def load_genesis_environment():

    load_dotenv()

    return {
        "openrouter": bool(
            os.getenv("OPENROUTER_API_KEY")
        ),

        "api_key":
            os.getenv("OPENROUTER_API_KEY")
    }


genesis_environment = load_genesis_environment()
