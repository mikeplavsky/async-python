from urllib import request, parse
from threading import Thread

import json
import sys

pt_url = "https://www.pivotaltracker.com/services/v5/projects"

def get(url, token):

    req = request.Request(
            url,
            headers={"X-TrackerToken":token})

    raw = request.urlopen(req)

    return  json.loads(
            raw.read().decode("utf-8"))

def get_releases(name, prj_id, token):

    url = "%s/%s/iterations?" % (pt_url, prj_id) 

    iters = []
    offset = 0

    while True:

        params = parse.urlencode(
                dict(
                    scope="current_backlog",
                    limit=100,
                    offset=offset))

        data = get(url+params, token)
        print(prj_id, offset, len(data))

        if len(data):
            iters.extend(data)

        else:
            break

        offset += len(data)

    return iters

def main(token):

    res = get(pt_url, token)
    [print(p['id'], p['name']) for p in res]

    threads = [
        Thread(
            target=get_releases,
            args=(p['name'], p['id'], token)) for p in res
    ]

    [t.start() for t in threads]
    [t.join() for t in threads]

main(sys.argv[1])

