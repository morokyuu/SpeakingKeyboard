# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 08:12:35 2023

@author: square


basics
https://grapebanana.com/python-encoding-utf-8-7161/

moji-code table
https://pentan.info/doc/unicode_list.html
"""


import re


# spell ='きくますとのは゜てみし゛らたす゛'
spell = 'は゜'
# spell = 'ぱ'
code = spell.encode('cp932')
print(spell)
print(code)

result = re.sub(b'\x82\xcd\x81K', b'\x82\xcf', code)

print(result)
print(result.decode('cp932'))
