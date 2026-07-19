import time
import uuid


class GenesisAutomationFactory:

    def __init__(self):

        self.system = "GENESIS AUTOMATION FACTORY v1"

        self.automations = []



    def create_automation(
        self,
        name,
        trigger,
        action,
        agent,
        skill
    ):

        automation = {

            "id":
            "automation_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "trigger":
            trigger,

            "action":
            action,

            "agent":
            agent,

            "skill":
            skill,

            "version":
            "v1.0",

            "status":
            "CREATED",

            "timestamp":
            time.time()

        }


        self.automations.append(automation)


        print(
            f"🏭 Automation created: {name}"
        )


        return automation



    def activate(
        self,
        automation_id
    ):

        for automation in self.automations:

            if automation["id"] == automation_id:

                automation["status"] = "ACTIVE"

                automation["activated"] = time.time()


                print(
                    f"✅ Automation activated: {automation['name']}"
                )


                return automation


        return {
            "status":
            "NOT_FOUND"
        }



    def list_automations(self):

        return self.automations



    def status(self):

        return {

            "system":
            self.system,

            "automations":
            len(self.automations),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



automation_factory = GenesisAutomationFactory()
