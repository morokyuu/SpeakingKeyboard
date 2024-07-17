# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 02:59:40 2024

@author: square

カタカナ変換を有効にする場合はkatakana_enb.csvに番号を登録する。
has_katakanaが１の時カタカナ変換が有効、０の時は無効。

wordsテーブルとidで INNER JOINするので、
katanakaに登録されている単語だけがJOINで拾われる。
has_katakanaを０で登録してもあんまり使い道はない。
いちおうwhere has_katakana=1 でフィルタはする。
"""

import sqlite3
import pandas as pd

df = pd.read_csv("katakana_enb.csv") ## カタカナ変換を有効にする場合はこのcsvに登録
df.columns = ['id','has_katakana']

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    df.to_sql('katakana',conn,if_exists='replace',index=None)
    print(df)
