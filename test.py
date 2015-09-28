import asyncio
import sys

async def slow_op(n):

    await asyncio.sleep(5)
    print("Done", n)

async def main():

    await asyncio.wait(
            [slow_op(i) for i in range(0,int(sys.argv[1]))])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
