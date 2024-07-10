# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 16:55:03 2024

@author: square
"""

dct = {'a':"あ",'i':"い"}

try:
    label = dct['b']
except:
    label = "なし"


try:
    label = dct['b']
finally:
    label = "なし"
## exceptがないと、このまま例外が発生する
