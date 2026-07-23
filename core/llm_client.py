import httpx
import yaml
import os
from dotenv import load_dotenv


class LLMClient:

    def __init__(self):

        root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        config_path = os.path.join(
            root,
            "config",
            "settings.yaml"
        )

        env_path = os.path.join(
            root,
            ".env"
        )

        if os.path.exists(env_path):
            load_dotenv(env_path)

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["llm"]

        self.provider = self.config["provider"]
        self.base_url = self.config["base_url"]

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY missing"
            )

        self.models = {

            "reasoning":
            "nvidia/nemotron-3-super-120b-a12b:free",

            "coding":
            "openai/gpt-oss-20b:free",

            "general":
            "google/gemma-4-31b-it:free",

            "fallback":
            "openrouter/free"

        }

        print(
            "🧠 Genesis LLM Council Online"
        )

        print(
            self.models
        )


    async def generate(
        self,
        prompt: str,
        system_prompt: str =
        "You are an expert AI agent.",
        task_type: str = "general",
        max_tokens: int = 4000
    ):

        preferred = self.models.get(
            task_type,
            self.models["general"]
        )

        fallback_chain = [
            preferred,
            self.models["general"],
            self.models["fallback"]
        ]

        last_error = None


        async with httpx.AsyncClient(
            timeout=120
        ) as client:


            for model in fallback_chain:

                try:

                    print(
                        f"🤖 Genesis trying model: {model}"
                    )


                    response = await client.post(

                        f"{self.base_url}/chat/completions",

                        headers={

                            "Authorization":
                            f"Bearer {self.api_key}",

                            "Content-Type":
                            "application/json",

                            "HTTP-Referer":
                            "https://agent-x.local",

                            "X-Title":
                            "Genesis-Core"

                        },

                        json={

                            "model":
                            model,

                            "messages":[

                                {
                                "role":
                                "system",

                                "content":
                                system_prompt
                                },

                                {
                                "role":
                                "user",

                                "content":
                                prompt
                                }

                            ],

                            "max_tokens":
                            max_tokens

                        }

                    )


                    if response.status_code == 200:

                        data=response.json()

                        print(
                            f"✅ Genesis model success: {model}"
                        )

                        return (
                            data["choices"][0]
                            ["message"]
                            ["content"]
                        )


                    else:

                        print(
                            f"⚠️ Model failed {model}: {response.status_code}"
                        )

                        last_error=response.text


                except Exception as e:

                    last_error=str(e)


        raise RuntimeError(
            f"All Genesis models failed: {last_error}"
        )


llm = LLMClient()
