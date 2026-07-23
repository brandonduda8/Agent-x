import time
import uuid


class GenesisJobMarketScanner:

    def __init__(self):
        self.sources = []
        self.jobs = []
        self.matches = []
        self.queue = []


    def add_job_source(
        self,
        name,
        category
    ):

        source = {
            "id": f"source_{uuid.uuid4().hex[:8]}",
            "name": name,
            "category": category,
            "status": "ACTIVE",
            "timestamp": time.time()
        }

        self.sources.append(source)

        return source


    def scan_market(
        self,
        category,
        keywords
    ):

        discovered = []

        templates = [
            {
                "title": "Warehouse Associate",
                "category": "Warehouse",
                "pay": 22
            },
            {
                "title": "Package Handler",
                "category": "Logistics",
                "pay": 20
            },
            {
                "title": "Shipping Receiving Associate",
                "category": "Warehouse",
                "pay": 23
            },
            {
                "title": "Customer Support Representative",
                "category": "Remote",
                "pay": 18
            }
        ]

        for item in templates:

            if category.lower() in item["category"].lower() or category == "ALL":

                job = {
                    "id": f"job_{uuid.uuid4().hex[:8]}",
                    "title": item["title"],
                    "category": item["category"],
                    "pay": item["pay"],
                    "keywords": keywords,
                    "status": "FOUND",
                    "timestamp": time.time()
                }

                self.jobs.append(job)
                discovered.append(job)


        return {
            "id": f"scan_{uuid.uuid4().hex[:8]}",
            "category": category,
            "jobs_found": len(discovered),
            "jobs": discovered,
            "status": "COMPLETE",
            "timestamp": time.time()
        }


    def match_jobs(
        self,
        skills
    ):

        results = []

        for job in self.jobs:

            score = 50

            for skill in skills:

                if skill.lower() in job["category"].lower():
                    score += 20


            match = {
                "job": job["id"],
                "title": job["title"],
                "score": min(score,100),
                "priority": "HIGH" if score >=80 else "MEDIUM"
            }

            self.matches.append(match)
            results.append(match)


        return {
            "matches": results,
            "status": "READY",
            "timestamp": time.time()
        }


    def create_application_queue(self):

        self.queue = sorted(
            self.matches,
            key=lambda x: x["score"],
            reverse=True
        )

        return {
            "queue": self.queue,
            "status": "READY",
            "timestamp": time.time()
        }


    def report(self):

        return {
            "system": "GENESIS JOB MARKET SCANNER v1",
            "sources": len(self.sources),
            "jobs": len(self.jobs),
            "matches": len(self.matches),
            "queue": len(self.queue),
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_job_market_scanner = GenesisJobMarketScanner()
