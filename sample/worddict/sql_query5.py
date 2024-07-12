# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:26:18 2024

@author: square
"""


import sqlite3


targ = ('り%',)

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    
    ## 下記1,2を別々に実行すると、動作がよくわかる
    
    ## 1> likeにより "りんご","りょこう","りす"がのこる
    # cur.execute("select * from words inner join katakana_flag on words.id = katakana_flag.id where words.word like ?",targ)
    ## 2> has_katakana=1の条件を追加すると、"りょこう"はhas_katakana=0なので除外されて、"りす","りんご"がのこる
    cur.execute("select * from words inner join katakana_flag on words.id = katakana_flag.id where words.word like ? and katakana_flag.has_katakana = 1",targ)
    
    
    for row in cur:
        print(row)
    
    