import asyncio
from core.genesis.genesis_kernel import genesis_kernel


async def main():

    print(await genesis_kernel.start())

    print(
        await genesis_kernel.emit(
            "TEST_EVENT",
            {
                "message": "Genesis OS v2 is alive"
            }
        )
    )

    print(genesis_kernel.report())


asyncio.run(main())
