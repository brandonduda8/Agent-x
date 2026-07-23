import time
import uuid


class GenesisJobAdapterNetwork:

    def __init__(self):
        self.adapters = []
        self.jobs = []


    def register_adapter(
        self,
        name,
        source_type
    ):

        adapter = {
            "id": f"adapter_{uuid.uuid4().hex[:8]}",
            "name": name,
            "type": source_type,
            "status": "CONNECTED",
            "timestamp": time.time()
        }

        self.adapters.append(adapter)

        return adapter


    def ingest_job(
        self,
        adapter,
        title,
        company,
        pay,
        category
    ):

        job = {
            "id": f"job_{uuid.uuid4().hex[:8]}",
            "adapter": adapter,
            "title": title,
            "company": company,
            "pay": pay,
            "category": category,
            "status": "NORMALIZED",
            "timestamp": time.time()
        }

        self.jobs.append(job)

        return job


    def search_results(self):

        return {
            "jobs": self.jobs,
            "count": len(self.jobs),
            "status": "READY",
            "timestamp": time.time()
        }


    def report(self):

        return {
            "system": "GENESIS JOB ADAPTER NETWORK v1",
            "adapters": len(self.adapters),
            "jobs": len(self.jobs),
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_job_adapter_network = GenesisJobAdapterNetwork()
