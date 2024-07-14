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
    
    ## 1> JOINした後、whereでLIKE検索する場合。
    cur.execute("select * from words inner join katakana on words.id = katakana.id where words.word like ?",targ)
    ## 2> 1の条件に、has_katakana=1の条件を追加
    # cur.execute("select * from words inner join katakana on words.id = katakana.id where words.word like ? and katakana.has_katakana = 1",targ)
    
    
    for row in cur:
        print(row)
    
    