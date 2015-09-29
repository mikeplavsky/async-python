from urllib import request, parse
from threading import Thread
import queue

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

def get_releases(name, prj_id, token, q, p):

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
        p.put((prj_id, offset, len(data)))

        if len(data):
            iters.extend(data)

        else:
            break

        offset += len(data)

    q.put((name, len(iters)))

def main(token):

    res = get(pt_url, token)
    [print(p['id'], p['name']) for p in res]

    qu = queue.Queue()
    pr = queue.Queue()

    threads = [
        Thread(
            target=get_releases,
            args=(
                p['name'], 
                p['id'], 
                token, qu, pr)) for p in res
    ]

    def progress():

        while True:
           print(pr.get())

    pt = Thread(target=progress)

    pt.daemon = True
    pt.start()

    [t.start() for t in threads]
    [t.join() for t in threads]

    for t in threads:

        r = qu.get()
        print(r)

main(sys.argv[1])

