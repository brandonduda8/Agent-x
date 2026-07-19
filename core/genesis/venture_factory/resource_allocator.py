import time
import uuid


class ResourceAllocator:

    def __init__(self):
        self.system = "GENESIS RESOURCE ALLOCATOR v1"


    def allocate(self, company):

        resources = {
            "id": "allocation_" + uuid.uuid4().hex[:8],
            "company": company["name"],
            "agents": [
                "Sales Agent",
                "Automation Agent",
                "Deployment Agent",
                "Support Agent"
            ],
            "priority": "HIGH",
            "status": "ALLOCATED",
            "timestamp": time.time()
        }

        print(
            "🤖 Workforce allocated"
        )

        return resources


resource_allocator = ResourceAllocator()
