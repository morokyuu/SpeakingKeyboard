# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 23:56:25 2024

@author: square
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




df = pd.read_csv("katakana_enb.csv") ## カタカナ変換を有効にする場合はこのcsvに登録
df.columns = ['id','has_katakana']

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    df.to_sql('katakana',conn,if_exists='replace',index=None)
    print(df)
