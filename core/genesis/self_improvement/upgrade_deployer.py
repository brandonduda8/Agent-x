import uuid
import time


class UpgradeDeployer:

    def deploy(self, upgrade):

        result = {
            "id": f"deployment_{uuid.uuid4().hex[:8]}",
            "upgrade": upgrade["name"],
            "status":"DEPLOYED",
            "timestamp":time.time()
        }

        print(
            "🚀 Upgrade deployed"
        )

        return result


upgrade_deployer = UpgradeDeployer()
