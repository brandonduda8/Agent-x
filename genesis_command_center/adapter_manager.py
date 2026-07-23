import datetime


class Adapter:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.status = "ONLINE"

    def execute(self, task):

        return {
            "adapter": self.name,
            "task": task,
            "timestamp": str(datetime.datetime.now()),
            "status": "COMPLETED"
        }


class AdapterManager:

    def __init__(self):

        self.adapters = {}

    def register(self, adapter):

        self.adapters[adapter.name] = adapter

    def list_adapters(self):

        return {
            name:{
                "category":adapter.category,
                "status":adapter.status
            }
            for name,adapter in self.adapters.items()
        }

    def run(self, adapter_name, task):

        adapter = self.adapters.get(adapter_name)

        if not adapter:

            return {
                "status":"ERROR",
                "message":"Adapter not found"
            }

        return adapter.execute(task)



if __name__ == "__main__":

    manager = AdapterManager()


    manager.register(
        Adapter(
            "Job Discovery Adapter",
            "income"
        )
    )


    manager.register(
        Adapter(
            "Housing Resource Adapter",
            "housing"
        )
    )


    manager.register(
        Adapter(
            "Business Lead Adapter",
            "revenue"
        )
    )


    print(manager.list_adapters())


    print(
        manager.run(
            "Job Discovery Adapter",
            "Find matching opportunities"
        )
    )
