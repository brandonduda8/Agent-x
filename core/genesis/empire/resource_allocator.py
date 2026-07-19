import time
import uuid


class ResourceAllocator:

    def __init__(self):
        self.system = "GENESIS RESOURCE ALLOCATOR v1"


    def allocate(
        self,
        companies,
        agents
    ):

        allocation = []

        for company in companies:

            allocation.append(
                {
                    "company": company["name"],
                    "agents_allocated": agents,
                    "priority": company["potential"]
                }
            )

        result = {
            "id": "allocation_" + uuid.uuid4().hex[:8],
            "allocation": allocation,
            "status": "COMPLETE",
            "timestamp": time.time()
        }

        print(
            "⚖️ Resources allocated"
        )

        return result


resource_allocator = ResourceAllocator()
