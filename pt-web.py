import aiohttp
import asyncio
import json
import sys

pt_url = "https://www.pivotaltracker.com/services/v5/projects"

async def get(url, token, data = None):

    hs = {"X-TrackerToken" : token}
    
    res = await aiohttp.get(url, headers=hs, params=data)
    return json.loads( await res.text() )

async def get_releases(name, prj_id, token):

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

    return (name, len(rs))

async def projects(token):

    data = await get(pt_url, token)
    [print(p['id'], p['name']) for p in data]

async def main(token):

    data = await get(pt_url, token)
    [print(p['id'], p['name']) for p in data]

    done, _ = await asyncio.wait([

            get_releases(
                p['name'], p['id'], token
                ) for p in data    

        ])

    [print(*r.result()) for r in done]


import os

token = os.environ["PT_TOKEN"]
project = os.environ.get("PT_PROJECT")

loop = asyncio.get_event_loop()


if not project: 

    loop.run_until_complete(
            projects(token))

else:

    print(project)

