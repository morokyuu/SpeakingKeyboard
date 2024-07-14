# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 12:22:59 2024

@author: square


パターンの指定をパラメータとして渡す場合のやり方
sqlite3 passing parameter
https://docs.python.org/3.10/library/sqlite3.html#sqlite3-howtos
"""


import sqlite3


targ = ('すず%',)

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    cur.execute("select * from words where word like ?", targ)
    for row in cur:
        print(row)