class IntelligenceRouter:

    def __init__(self):

        self.routes = {

            "research":
                "deepseek/deepseek-chat-v3-0324",

            "strategy":
                "deepseek/deepseek-chat-v3-0324",

            "coding":
                "qwen/qwen2.5-coder-32b-instruct",

            "general":
                "meta-llama/llama-3.1-8b-instruct",

            "revenue":
                "deepseek/deepseek-chat-v3-0324"

        }


    def select_model(
        self,
        task_type
    ):

        return self.routes.get(
            task_type,
            self.routes["general"]
        )


    def explain(
        self,
        task_type
    ):

        model = self.select_model(
            task_type
        )

        return {

            "task":
                task_type,

            "selected_model":
                model,

            "reason":
                "Optimized by Genesis Intelligence Router"

        }



intelligence_router = IntelligenceRouter()
