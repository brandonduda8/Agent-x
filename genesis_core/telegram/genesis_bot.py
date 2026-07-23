from genesis_core.telegram.command_router import GenesisCommandRouter



class GenesisTelegramInterface:


    def __init__(
        self,
        state
    ):

        self.router = GenesisCommandRouter(
            state
        )



    def receive(
        self,
        message
    ):

        return self.router.route(
            message
        )
