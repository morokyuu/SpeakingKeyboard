# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 06:46:26 2024

@author: square

https://tipstour.net/python-pandas-get-value
"""

import pandas as pd

df = pd.read_csv('words.csv', encoding="shift-jis", delimiter='\t')

df[df['kind']==1]['word']

s = df['word']

a = df.loc[s.str.startswith('あ')]

print(a['word'])




# print(a['word'].loc[])


length = df[df['kind']<2]['word'].shape[0]
b = df[df['kind']<2]['word']
for i in range(length):
    print(b[i])


# length = df[df['kind']>1]['word'].shape[0]
# c = df[df['kind']>1]['word']
# for i in range(length):
#     print(c[i])

# words = df[df['kind']>1]['word']
# # print(words[0])
# length = words.shape[0]


# w = [words[i] for i in range(length)]