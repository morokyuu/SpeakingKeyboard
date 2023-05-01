## ref
##  https://qiita.com/tchnkmr/items/b05f321fa315bbce4f77
##  https://magazine.techacademy.jp/magazine/22221

from threading import Thread

import time

class Worker(Thread):
    def __init__(self,name):
        super(Worker, self).__init__()
        self.name = name
    def run(self):
        print(f'my name is {self.name}')
        print("zzz")
        for _ in range(3):
            print("zzz")
            time.sleep(1)

w1 = Worker("hoge")
w1.start()

w2 = Worker("muga")
w2.start()

w3 = Worker("migu")
w3.start()

