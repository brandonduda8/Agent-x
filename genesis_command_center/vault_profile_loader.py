import json


with open("vault_profile.json", "r") as file:
    profile = json.load(file)


print({
    "system": "GENESIS VAULT PROFILE",
    "status": "ONLINE",
    "operator": profile["operator_profile"]["name"],
    "communication": profile["genesis_preferences"]["communication_channel"],
    "objectives": profile["genesis_preferences"]["primary_objectives"]
})
