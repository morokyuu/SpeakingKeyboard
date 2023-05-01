## ref
##  https://qiita.com/tchnkmr/items/b05f321fa315bbce4f77
##

from threading import Thread

import time


def work(name):
    print(f'my name is {name}')
    print("zzz")
    for _ in range(3):
        print("zzz")
        time.sleep(1)

t = Thread(target=work, args=("hoge",))
t2 = Thread(target=work, args=("foo",))

t.start()
t2.start()


