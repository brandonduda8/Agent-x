import httpx
import yaml
import json
import os

class LLMClient:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config/settings.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['llm']
            
        self.provider = self.config['provider']
        self.model = self.config['model']
        self.base_url = self.config['base_url']
        
        env_path = "/data/data/com.termux/files/home/agent-x/.env"
        self.api_key = None
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f.read().splitlines():
                    line = line.strip().replace('\r', '')
                    if line.startswith('OPENROUTER_API_KEY='):
                        self.api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
        
        if not self.api_key and self.provider == "openrouter":
            raise ValueError("⚠️ OPENROUTER_API_KEY not found or invalid in .env file!")
            
        print(f"🔑 [LLM] Successfully loaded API key: {self.api_key[:15]}...")

    async def generate(self, prompt: str, system_prompt: str = "You are an expert AI agent.", max_tokens: int = 8000) -> str:
        print(f"🧠 [LLM] Thinking with {self.model} via OpenRouter (max_tokens={max_tokens})...")
        
        if self.provider == "openrouter":
            return await self._call_openrouter(prompt, system_prompt, max_tokens)
        else:
            return await self._call_ollama(prompt, system_prompt)

    async def _call_openrouter(self, prompt: str, system_prompt: str, max_tokens: int) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions", 
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://agent-x.local",
                    "X-Title": "Agent-X Autopilot"
                },
                json={
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            if response.status_code != 200:
                raise Exception(f"OpenRouter API Error: {response.text}")
                
            return response.json()['choices'][0]['message']['content']

    async def _call_ollama(self, prompt: str, system_prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{self.base_url}/api/chat", json={
                "model": self.model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            })
            return response.json()['message']['content']

llm = LLMClient()
