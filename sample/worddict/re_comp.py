# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 22:33:53 2024

@author: square
"""

import re

dat = r"""
あさがお
あさひ
いか
なんこつ
すし
すいか
すいとう
うかい
うし
しゅうまい
いかなご
ほうすい
"""

# dat = """
# book
# boot
# bike
# """


pat = re.compile(r'すい.*')
print(pat.findall(dat))

pat = re.compile(r'あさ.*')
print(pat.findall(dat))

for d in dat.split():
    if d.startswith("すい"):
        print(d)
