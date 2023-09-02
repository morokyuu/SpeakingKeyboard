# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 15:56:34 2023

@author: square
"""

import re

with open("kana-dict.txt","r") as fp:
    words = [l.rstrip() for l in fp.readlines()]


    
text = "なす"
pat = re.compile(text)

for w in words:
    if re.match(pat,w):
        print(w)

print("full match---")
for w in words:
    if re.fullmatch(pat,w):
        print(w)
