## ref
##  timer
##  https://docs.python.org/ja/3/library/threading.html

from threading import Thread
from threading import Timer

import time

def hello():
    print("hello")


t = Timer(10.0, hello)
t.start()

for _ in range(8):
    print("wait")
    time.sleep(1)

