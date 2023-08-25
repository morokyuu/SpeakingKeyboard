# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 08:12:35 2023

@author: square


basics
https://grapebanana.com/python-encoding-utf-8-7161/

moji-code table
https://pentan.info/doc/unicode_list.html

文字コード表に載ってるbinaryをそのまま使うとencode()の”x81K”とか出た場合どうするか問題に当たるので、
並び順や値の確認だけ使うことにしておき、コードはあくまでencode()で作って、それと入力ラベルを比較するのがいい。
"""


import re


before = 'かきくけこさしすせそたちつてとはひふへほ'
after = 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'

dakuten = []
for b,a in zip(before,after):
    bcode = b.encode('cp932') + '゛'.encode('cp932')
    acode = a.encode('cp932')
    # print(f"{b}゛,{a},{bcode},{acode}")
    dakuten.append((bcode,acode))

before = 'はひふへほ'
after = 'ぱぴぷぺぽ'

handakuten = []
for b,a in zip(before,after):
    bcode = b.encode('cp932') + '゜'.encode('cp932')
    acode = a.encode('cp932')
    # print(f"{b}゜,{a},{bcode},{acode}")
    handakuten.append((bcode,acode))

tr_table = dakuten + handakuten


# result = re.sub(b'\x82\xcd\x81K', b'\x82\xcf', code)

st = "は゜いなっふ゜る"
st = st.encode('cp932')
for b,a in tr_table:
    st = re.sub(b,a,st)


print(st)
print(st.decode('cp932'))


