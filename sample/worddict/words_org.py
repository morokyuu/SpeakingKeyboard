# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 23:56:25 2024

@author: square

単語をCSVから読み込んでデータベースに登録するスクリプト
CSVに書かれている単語を読み取りデータベース化する。

words_org.csvがメインの単語データ。
idはテキストファイルに直書きすることで、関連テーブルとの紐づけが切れないようにする。
"""

import sqlite3
import pandas as pd

df = pd.read_csv("words_org.csv") ## このファイルがデータベースの元ファイル
df.columns = ['id','word']

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    df.to_sql('words',conn,if_exists='replace',index=None)
    print(df)



