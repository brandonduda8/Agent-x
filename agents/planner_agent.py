import asyncio

async def planner(event):

    print(
        "[PLANNER]",
        event["payload"]
    )

    await asyncio.sleep(2)

    print(
        "[PLANNER] complete"
    )
