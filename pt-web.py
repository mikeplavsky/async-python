import aiohttp
import asyncio
import json
import sys

pt_url = "https://www.pivotaltracker.com/services/v5/projects"

async def main(token):

    hs = {"X-TrackerToken" : token}

    res = await aiohttp.get(pt_url, headers=hs)
    data = json.loads( await res.text())

    [print(p['name']) for p in data]

loop = asyncio.get_event_loop()
loop.run_until_complete(main(sys.argv[1]))
