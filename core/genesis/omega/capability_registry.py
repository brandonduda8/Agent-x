import os
import json
import time
import uuid


class GenesisOmegaCapabilityRegistry:
    """
    GENESIS OMEGA CAPABILITY REGISTRY v2

    Persistent capability discovery layer.

    Tracks:
    - capabilities
    - providers
    - descriptions
    - priorities
    - health
    - history
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA CAPABILITY REGISTRY v2"
        )

        self.file = (
            "data/genesis_omega_capabilities.json"
        )

        self.registry = {}

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()

        self.bootstrap_defaults()


    def load(self):

        if os.path.exists(
            self.file
        ):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    data = json.load(f)

                    self.registry = data.get(
                        "registry",
                        {}
                    )

            except Exception:

                self.registry = {}


    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                {
                    "system":
                        self.system,

                    "registry":
                        self.registry,

                    "updated":
                        time.time()
                },
                f,
                indent=2
            )


    def register(
        self,
        capability,
        provider,
        description="",
        priority=50
    ):

        entry = {

            "id":
                "capability_"
                + uuid.uuid4().hex[:8],

            "capability":
                capability,

            "provider":
                provider,

            "description":
                description,

            "priority":
                priority,

            "status":
                "AVAILABLE",

            "updated":
                time.time()

        }

        self.registry[capability] = entry

        self.save()

        return entry


    def find(
        self,
        capability
    ):

        return self.registry.get(
            capability
        )


    def list_capabilities(self):

        return list(
            self.registry.values()
        )


    def bootstrap_defaults(self):

        defaults = [

            (
                "revenue",
                "Genesis Revenue Operator",
                "Revenue strategy, sales, offers, client conversion",
                90
            ),

            (
                "real_world_execution",
                "Genesis Reality Action Engine",
                "Execute real world action workflows",
                80
            ),

            (
                "mission_execution",
                "Genesis Execution Systems",
                "Convert missions into executable tasks",
                85
            ),

            (
                "opportunity_discovery",
                "Genesis Opportunity Hunter",
                "Discover opportunities and markets",
                75
            ),

            (
                "memory",
                "Genesis Memory Layer",
                "Store learning and historical knowledge",
                70
            )

        ]


        changed = False


        for item in defaults:

            capability = item[0]

            if capability not in self.registry:

                self.register(
                    item[0],
                    item[1],
                    item[2],
                    item[3]
                )

                changed = True


        if changed:

            self.save()


    def report(self):

        return {

            "system":
                self.system,

            "capabilities":
                len(
                    self.registry
                ),

            "available":
                list(
                    self.registry.keys()
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }


genesis_omega_capability_registry = (
    GenesisOmegaCapabilityRegistry()
)
