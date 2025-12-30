# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:31:39 2024

@author: square

正規表現で検索
regexpでやろうとしたらうまくいかず。
https://stackoverflow.com/questions/5071601/how-do-i-use-regex-in-a-sqlite-query

likeのほうがうまくマッチさせることができて、今の用途にはちょうどよいことがわかった。これだけで十分できる。
https://www.javadrive.jp/sqlite/select/index6.html
"""

import sqlite3

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    cur.execute("select * from words where word like 'すず%'")
    # cur.execute("select * from words where words.word REGEXP 'すず*'") ##error
    for row in cur:
        print(row)