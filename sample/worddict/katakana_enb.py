import sqlite3
import pandas as pd

df = pd.read_csv("kata2")
df.columns = ['id','has_katakana']


df = df.replace('-',False)
# df[df['has_katakana'] == '-'] = False
# df[df['has_katakana'] != False] = True

df.loc[df.has_katakana != False, 'has_katakana'] = True

print(df)

# dbname = 'tango.db'
# with sqlite3.connect(dbname) as conn:
#     cur = conn.cursor()
#     df.to_sql('katakana_flag',conn,if_exists='replace',index=None)
#     print(df)

