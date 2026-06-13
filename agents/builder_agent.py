import asyncio

async def builder(event):

    print(
        "[BUILDER]",
        event["payload"]
    )

    await asyncio.sleep(1)

    print(
        "[BUILDER] complete"
    )
