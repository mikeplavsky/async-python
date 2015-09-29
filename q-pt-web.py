import aiohttp
import asyncio
import json
import sys

pt_url = "https://www.pivotaltracker.com/services/v5/projects"

async def get(url, token, data = None):

    hs = {"X-TrackerToken" : token}
    
    res = await aiohttp.get(url, headers=hs, params=data)
    return json.loads( await res.text() )

async def get_releases(name, prj_id, token, q, p):

    rs = []
    offset = 0

    while True:

        url = "%s/%s/iterations?" % (pt_url, prj_id) 
        
        data = dict(
                scope="current_backlog", 
                limit=100,
                offset=offset)

        data = await get(url, token, data)

        await p.put(
                (prj_id, offset, len(data)))

        if (len(data)):
            rs.extend(data)

        else:
            break

        offset += len(data)

    await q.put(
            (name, len(rs)))


async def progress(p):
    
    while True:
        print(await p.get())

async def main(token):

    data = await get(pt_url, token)

    [print(p['id'], p['name']) for p in data]

    qu = asyncio.Queue(maxsize=len(data))
    pr = asyncio.Queue()

    pr_t = asyncio.ensure_future(progress(pr))

    await asyncio.wait([

            get_releases(
                p['name'], p['id'], token, qu, pr
                ) for p in data    

        ])

    for i in range(0,len(data)):

            r = await qu.get()
            print(*r)

    pr_t.cancel()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(sys.argv[1]))
