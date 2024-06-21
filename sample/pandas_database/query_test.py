# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 06:46:26 2024

@author: square
"""

import pandas as pd

df = pd.read_csv('words.csv', encoding="shift-jis", delimiter='\t')

#a = df.loc[df['kind']==1,df.columns.str.startswith('あ')]


s = df['word']

a = df.loc[s.str.startswith('あ')]

print(a['word'])

print(a['word'].loc[-1])
    