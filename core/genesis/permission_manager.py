import time


class GenesisPermissionManager:

    def __init__(self):

        self.system = "GENESIS PERMISSION MANAGER v1"

        self.permissions = {}


    def register_agent(
        self,
        agent,
        permissions
    ):

        self.permissions[agent] = permissions


        print(
            f"🔐 Permissions registered: {agent}"
        )


        return {

            "agent": agent,

            "permissions": permissions,

            "timestamp": time.time()

        }



    def check(
        self,
        agent,
        permission
    ):

        allowed = (
            permission in
            self.permissions.get(agent, [])
        )


        return {

            "agent":
            agent,

            "permission":
            permission,

            "allowed":
            allowed,

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "agents":
            len(self.permissions),

            "timestamp":
            time.time()

        }



permission_manager = GenesisPermissionManager()
