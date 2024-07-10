import sqlite3
import pandas as pd

#df = pd.read_csv("kana-dict.txt",delimiter=',')
df = pd.read_csv("kana-dict.txt")
df.columns = ['hiragana','katakana']

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    df.to_sql('sample',conn,if_exists='replace')
    print(df)

