class GenesisOmegaWorkerContract:
    """
    GENESIS OMEGA WORKER CONTRACT v1

    Standard interface every Omega worker should expose.
    """

    name = "UNKNOWN_WORKER"

    def execute(self, task):
        raise NotImplementedError(
            "Omega worker must implement execute()"
        )
