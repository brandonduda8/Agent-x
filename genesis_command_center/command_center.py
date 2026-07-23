import json
import os
from datetime import datetime

BASE = os.path.dirname(__file__)

def load(name):
    with open(os.path.join(BASE,name)) as f:
        return json.load(f)

def status():
    return {
        "system":"GENESIS COMMAND CENTER",
        "time":str(datetime.now()),
        "profile":load("profile.json"),
        "memory":load("memory.json"),
        "adapters":load("adapters.json")
    }

if __name__ == "__main__":
    print(json.dumps(status(),indent=2))
