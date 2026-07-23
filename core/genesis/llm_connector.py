import time
import uuid
import requests

from core.genesis.env_loader import genesis_environment


class GenesisLLMConnector:

    def __init__(self):

        self.system = "GENESIS LLM BRAIN MANAGER v7"
        self.executions = []

        self.models = {

            "coding": [
                "qwen/qwen3-coder",
                "qwen/qwen-2.5-coder-32b-instruct",
                "meta-llama/llama-3.1-8b-instruct"
            ],

            "reasoning": [
                "deepseek/deepseek-r1-0528",
                "deepseek/deepseek-r1",
                "qwen/qwen3-max-thinking"
            ],

            "architecture": [
                "nvidia/nemotron-3-super-120b-a12b:free",
                "qwen/qwen3-235b-a22b",
                "meta-llama/llama-4-maverick"
            ],

            "research": [
                "deepseek/deepseek-chat-v3-0324",
                "qwen/qwen3-30b-a3b",
                "meta-llama/llama-3.1-8b-instruct"
            ],

            "general": [
                "meta-llama/llama-3.1-8b-instruct",
                "qwen/qwen-2.5-7b-instruct"
            ]
        }


    def health_check(self):

        return {
            "system": self.system,
            "openrouter": genesis_environment["openrouter"],
            "models": sum(len(v) for v in self.models.values()),
            "timestamp": time.time()
        }


    def select_model(self, task):

        pool = self.models.get(
            task,
            self.models["general"]
        )

        return {
            "provider": "openrouter",
            "model": pool[0],
            "alternatives": pool[1:]
        }


    def extract_response(self, data):

        try:

            return (
                data
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content")
            )

        except:

            return None


    def call_model(self, model, prompt, tokens=1200):

        url = "https://openrouter.ai/api/v1/chat/completions"


        headers = {

            "Authorization":
            f"Bearer {genesis_environment['api_key']}",

            "Content-Type":
            "application/json"
        }


        payload = {

            "model": model,

            "messages": [
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            "max_tokens": tokens,

            "temperature":0.4
        }


        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )


        return response.json()



    def complete(self, task_type, prompt):

        selected = self.select_model(task_type)


        models = (
            [selected["model"]]
            +
            selected["alternatives"]
        )


        token_levels = [
            1200,
            800,
            500
        ]


        last_error = None


        for model in models:

            for tokens in token_levels:

                try:

                    print(
                        "🧠 Genesis Brain Attempt:",
                        model,
                        "TOKENS:",
                        tokens
                    )


                    raw = self.call_model(
                        model,
                        prompt,
                        tokens
                    )


                    content = self.extract_response(raw)


                    if content:

                        result = {

                            "id":
                            "llm_" +
                            uuid.uuid4().hex[:8],

                            "task":
                            task_type,

                            "model":
                            model,

                            "status":
                            "SUCCESS",

                            "output":
                            content,

                            "timestamp":
                            time.time()
                        }


                        self.executions.append(result)

                        return result



                    last_error = raw


                except Exception as e:

                    last_error = str(e)



        result = {

            "id":
            "llm_" +
            uuid.uuid4().hex[:8],

            "task":
            task_type,

            "status":
            "FAILED",

            "error":
            last_error,

            "timestamp":
            time.time()
        }


        self.executions.append(result)


        return result



    def report(self):

        return {

            "system":
            self.system,

            "executions":
            len(self.executions),

            "timestamp":
            time.time()
        }



llm_connector = GenesisLLMConnector()
