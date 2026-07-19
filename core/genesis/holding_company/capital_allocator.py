import time
import uuid


class CapitalAllocator:

    def __init__(self):
        self.system = "GENESIS CAPITAL ALLOCATOR v1"


    def allocate(self, companies):

        allocation = []

        for company in companies:

            allocation.append({
                "company": company["company"],
                "priority": "HIGH",
                "resources": [
                    "Sales Agents",
                    "Automation Agents",
                    "Development Agents"
                ]
            })


        result = {
            "id": "capital_" + uuid.uuid4().hex[:8],
            "allocation": allocation,
            "status": "COMPLETE",
            "timestamp": time.time()
        }


        print(
            "💰 Capital resources allocated"
        )

        return result


capital_allocator = CapitalAllocator()
