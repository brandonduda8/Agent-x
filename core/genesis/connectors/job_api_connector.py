import time
import requests


class GenesisInternetJobConnector:

    """
    GENESIS INTERNET JOB CONNECTOR v1

    Pulls real public job feeds.
    """

    def __init__(self):
        self.system = "GENESIS INTERNET JOB CONNECTOR v1"
        self.jobs = []


    def fetch_remotive(self, search="python"):

        url = "https://remotive.com/api/remote-jobs"

        response = requests.get(
            url,
            params={
                "search": search
            },
            timeout=15
        )

        data = response.json()

        results = []

        for job in data.get("jobs", [])[:10]:

            results.append(
                {
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "url": job.get("url"),
                    "skills": [
                        search,
                        "remote"
                    ],
                    "source": "Remotive",
                    "created": time.time()
                }
            )

        self.jobs.extend(results)

        return results


    def report(self):

        return {
            "system": self.system,
            "jobs_found": len(self.jobs),
            "timestamp": time.time()
        }


job_api_connector = GenesisInternetJobConnector()
