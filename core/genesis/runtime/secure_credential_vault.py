import time
import uuid


class GenesisSecureCredentialVault:


    def __init__(
        self,
        store,
        permissions,
        audit
    ):

        self.store = store
        self.permissions = permissions
        self.audit = audit

        self.system = (
            "GENESIS SECURE CREDENTIAL VAULT v1"
        )


    def add(
        self,
        name,
        value
    ):

        result = self.store.store(
            name,
            value
        )

        self.audit.record(
            "Credential stored: " + name
        )

        return result



    def access(
        self,
        connector,
        credential
    ):

        permission = self.permissions.authorize(
            connector,
            credential
        )

        value = self.store.retrieve(
            credential
        )


        self.audit.record(
            "Credential accessed: " + credential
        )


        return {

            "id":
                "vault_" +
                uuid.uuid4().hex[:8],

            "permission":
                permission,

            "available":
                value is not None,

            "status":
                "ACCESS_GRANTED",

            "timestamp":
                time.time()

        }

