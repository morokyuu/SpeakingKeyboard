## prototype for tango.db
## DO NOT USE FOR APPENDING WORDS

import sqlite3
import pandas as pd

#df = pd.read_csv("kana-dict.txt",delimiter='\t')
df = pd.read_csv("hira2")
df.columns = ['id','word']

dbname = 'tango.db'
with sqlite3.connect(dbname) as conn:
    cur = conn.cursor()
    df.to_sql('words',conn,if_exists='replace',index=None)
    print(df)

