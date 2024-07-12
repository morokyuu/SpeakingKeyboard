# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:26:18 2024

@author: square
"""


import sqlite3


targ = ('あ%',)

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    
    cur.execute("select * from words inner join katakana_flag on words.id = katakana_flag.id where words.word like ? and katakana_flag.has_katakana = 1",targ)
    
    # cur.execute("select * from words inner join katakana_flag on words.id = katakana_flag.id where words.word like ? and katakana_flag.has_katakana = 1",targ)
    for row in cur:
        print(row)
    
    
    # print("--------")
    # cur.execute("select * from words inner join katakana_flag on words.id = katakana_flag.id")
    # for row in cur:
    #     print(row)
    
    # print("--------")
    # cur.execute("select word from words")
    # for row in cur:
    #     print(row)
    