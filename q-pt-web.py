import aiohttp
import asyncio
import json
import sys

pt_url = "https://www.pivotaltracker.com/services/v5/projects"

async def get(url, token, data = None):

    hs = {"X-TrackerToken" : token}
    
    res = await aiohttp.get(url, headers=hs, params=data)
    return json.loads( await res.text() )

async def get_releases(name, prj_id, token, q):

    rs = []
    offset = 0

    while True:

        url = "%s/%s/iterations?" % (pt_url, prj_id) 
        
        data = dict(
                scope="current_backlog", 
                offset=offset)

        data = await get(url, token, data)

        print(offset, len(data))

        if (len(data)):
            rs.extend(data)

        else:
            break

        offset += 10

    await q.put(
            (name, len(rs)))


async def main(token):

    data = await get(pt_url, token)

    [print(p['id'], p['name']) for p in data]

    q = asyncio.Queue(maxsize=len(data))

    await asyncio.wait([

            get_releases(
                p['name'], p['id'], token, q
                ) for p in data    

        ])

    for i in range(0,len(data)):

            r = await q.get()
            print(*r)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(sys.argv[1]))
