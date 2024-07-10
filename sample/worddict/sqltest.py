# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 23:33:27 2024

@author: square


sqlite3は標準ライブラリですぐに使える。
データベースの中身はローカルにファイルとして保存される。

https://toukei-lab.com/python-sqlite3
https://toukei-lab.com/sql-select%E6%96%87

"""

import sqlite3

conn = sqlite3.connect('tameshi.db')
cursor = conn.cursor()


sql = """CREATE TABLE IF NOT EXISTS test(id, name, date)"""
cursor.execute(sql)#executeコマンドでSQL文を実行


sql = """INSERT INTO test VALUES(?,?,?)"""

data = ((1,'Tama',1999))
cursor.execute(sql,data)
conn.commit()

