import time
import threading


def run(num):
    print(num)
    time.sleep(5)


_thread = []
for i in range(5):
    _thread.append(threading.Thread(target=run, args=(i,)))

for _t in _thread:
    _t.start()

for _t in _thread:
    _t.join()
