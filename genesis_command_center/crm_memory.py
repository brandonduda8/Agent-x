import json
from datetime import datetime


CRM_FILE = "crm_memory.json"


def load_crm():

    try:
        with open(CRM_FILE, "r") as f:
            return json.load(f)

    except:
        return {
            "leads": [],
            "metrics": {
                "total_leads": 0,
                "contacts_sent": 0,
                "responses": 0,
                "opportunities": 0
            }
        }


def add_lead(name, company, value):

    crm = load_crm()

    lead = {

        "id": len(crm["leads"]) + 1,

        "name": name,

        "company": company,

        "estimated_value": value,

        "status": "NEW",

        "last_action": "Created",

        "created": str(datetime.now())

    }


    crm["leads"].append(lead)

    crm["metrics"]["total_leads"] += 1


    with open(CRM_FILE, "w") as f:

        json.dump(crm, f, indent=4)


    return lead



if __name__ == "__main__":

    print(
        json.dumps(
            add_lead(
                "Example Contact",
                "Example Company",
                "$1000-$5000"
            ),
            indent=4
        )
    )
