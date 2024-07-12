# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:31:39 2024

@author: square

テーブルをjoinで結合した後、katakana_flag.has_katakana = 1のやつだけをフィルタして取ってくる。
"""

import sqlite3

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    cur.execute('select * from words inner join katakana_flag on words.id = katakana_flag.id where katakana_flag.has_katakana')
    for row in cur:
        print(row)