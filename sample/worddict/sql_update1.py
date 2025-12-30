# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 23:10:59 2024

@author: square

参考

UPDATE使い方
https://qiita.com/tsweblabo/items/a4b45cfc4d73b5b453fa
カウントアップの書き方  同じテーブルのcount項目をインクリメントしてUPDATEする方法は？
https://teratail.com/questions/14809
MIN,MAX関数の使い方
https://techmania.jp/blog/sql-count/#outline__2
公式。いろいろ発見がある
https://sqlite.org/lang.html
テスト用のデータを作ってくれるWEBサイト
https://generatedata.com/

existsを使って、データがあるかどうかを調べる方法
https://style.potepan.com/articles/19151.html
https://sql-jp.dev/articles/45156324
"""

import sqlite3


def printData(st,cur):
    print(f"---{st}")
    cur.execute("SELECT * FROM users")
    for row in cur:
        print(row)


def is_exists(id):
    exists = cur.execute("""
                SELECT EXISTS (
                    SELECT * FROM users
                    WHERE id = 4)
                """).fetchone()[0]
    print(f"EXISTS: {exists}")
    return exists

def countup(id):
    if is_exists(id):
        cur.execute('UPDATE users SET count = count + 1 WHERE id=?',(id,))
    else:
        cur.execute('INSERT INTO users (name,count) VALUES (?,?)',('Hishi',1))


dbname = ':memory:'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    count INTEGER NOT NULL)
    """)
    cur.execute('INSERT INTO users (name,count) VALUES (?,?)',('Hoge',20))
    cur.execute('INSERT INTO users (name,count) VALUES (?,?)',('Hoke',13))
    cur.execute('INSERT INTO users (name,count) VALUES (?,?)',('Hasu',19))
    
    printData("init",cur)
    
    ##これだと全員のカウントがアップする
    cur.execute('UPDATE users SET count = count + 1')
    printData("all countup",cur)

    ##これだとid=1のuserだけカウントアップ
    cur.execute('UPDATE users SET count = count + 1 where id=1')
    printData("only id=1 countup",cur)
    
    print("")
    ##id=4がいなければ追加、いればカウントアップ
    countup(4)
    printData("id=4 insert",cur)
    
    countup(4)
    printData("id=3 update",cur)
    
    a = cur.execute('SELECT COUNT(id) FROM users').fetchone()[0]
    
    b = cur.execute('SELECT COUNT(id) FROM (SELECT * FROM users where count > 10)').fetchone()[0]
    #a = cur.rowcount()
    
    