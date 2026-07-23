import json
from datetime import datetime


REGISTRY = "adapter_registry.json"


def load():

    try:
        with open(REGISTRY,"r") as f:
            return json.load(f)

    except:
        return {
            "system":"GENESIS ADAPTER REGISTRY",
            "adapters":[]
        }



def register(name, category, endpoint, permissions):

    data = load()

    adapter = {

        "name": name,
        "category": category,
        "endpoint": endpoint,
        "permissions": permissions,
        "status":"ONLINE",
        "connected":str(datetime.now())

    }

    data["adapters"].append(adapter)


    with open(REGISTRY,"w") as f:
        json.dump(data,f,indent=4)


    return adapter



if __name__=="__main__":

    print(
        register(
            "Phone Adapter",
            "device",
            "android-termux",
            ["notifications","commands"]
        )
    )
