
class GenesisCapabilityMap:


    def build(
        self,
        systems
    ):

        capabilities = {}


        for system in systems:

            for capability in system["capabilities"]:

                if capability not in capabilities:

                    capabilities[capability] = []


                capabilities[capability].append(
                    system["name"]
                )


        return capabilities
