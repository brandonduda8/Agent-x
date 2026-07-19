import httpx
import yaml
import os
from dotenv import load_dotenv

class LLMClient:
    def __init__(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        config_path = os.path.join(root, "config", "settings.yaml")
        env_path = os.path.join(root, ".env")

        if os.path.exists(env_path):
            load_dotenv(env_path)

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["llm"]

        self.provider = self.config["provider"]
        self.model = self.config["model"]
        self.base_url = self.config["base_url"]

        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if self.provider == "openrouter" and not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env")

        if self.api_key:
            print(f"🔑 Loaded OpenRouter key: {self.api_key[:12]}...")

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "You are an expert AI agent.",
        max_tokens: int = 8000,
    ) -> str:

        if self.provider == "openrouter":
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://agent-x.local",
                        "X-Title": "Agent-X",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt},
                        ],
                        "max_tokens": max_tokens,
                    },
                )

                response.raise_for_status()

                return response.json()["choices"][0]["message"]["content"]

        raise RuntimeError(f"Unsupported provider: {self.provider}")

llm = LLMClient()
