import asyncio

async def slow_op(n):
    await asyncio.sleep(1)
    print("Done", n)

async def main():

    await asyncio.wait(
            [slow_op(i) for i in range(0,10000)])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
