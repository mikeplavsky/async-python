from threading import Thread
import time
import sys

def slow_op(n):
    
    time.sleep(5)
    print("Done", n)

threads = []

def target(n):
    return lambda: slow_op(n)

for i in range(0,int(sys.argv[1])):

    t = Thread(target=target(i))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

