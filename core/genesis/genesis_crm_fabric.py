import time

from core.genesis.crm.local_crm import (
    local_crm
)


class GenesisCRMFabric:


    def __init__(self):

        self.system = (
            "GENESIS CRM FABRIC v1"
        )

        self.providers = {

            "local":
            local_crm

        }



    def create_lead(
        self,
        name,
        email="",
        company=""
    ):

        return (
            self.providers["local"]
            .create_contact(
                name,
                email,
                company
            )
        )



    def create_opportunity(
        self,
        contact_id,
        title,
        value
    ):

        return (
            self.providers["local"]
            .create_deal(
                contact_id,
                title,
                value
            )
        )



    def add_activity(
        self,
        activity,
        description
    ):

        return (
            self.providers["local"]
            .add_activity(
                activity,
                description
            )
        )



    def report(self):

        return {

            "system":
            self.system,

            "providers":
            list(
                self.providers.keys()
            ),

            "crm":
            self.providers["local"]
            .report(),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_crm_fabric = GenesisCRMFabric()
