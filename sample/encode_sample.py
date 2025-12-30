# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:24:48 2024

@author: square


濁点や半濁点を直前の仮名と結合させる方法
https://qiita.com/gretchi/items/13c0825282415e2e360d

結合文字列　Unicode
https://tama-san.com/combining_character_sequence/
"""


## 仮名をエンコードしてバイナリにする
enc_kana = "あいうえお".encode('cp932')
print(enc_kana)
## 
kana = enc_kana.decode('cp932')
print(kana)


## は (ha)
kana = b'\x82\xcd'.decode('cp932')
print(kana)
## は゜(ha,maru) 2 multi byte characters
kana = b'\x82\xcd\x81K'.decode('cp932')
print(kana)
## は゜(pa)
kana = b'\x82\xcf'.decode('cp932')
print(kana)

print("-------------")

# before = 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ'
# x = [b+'゛' for b in before]
# print(x)
before = 'はひふへほハヒフヘホ'
x = [b+'゜' for b in before]
print(x)

dakuten = ['か゛', 'き゛', 'く゛', 'け゛', 'こ゛', 'さ゛', 'し゛', 'す゛', 'せ゛', 'そ゛', 'た゛', 'ち゛', 'つ゛', 'て゛', 'と゛', 'は゛', 'ひ゛', 'ふ゛', 'へ゛', 'ほ゛', 'カ゛', 'キ゛', 'ク゛', 'ケ゛', 'コ゛', 'サ゛', 'シ゛', 'ス゛', 'セ゛', 'ソ゛', 'タ゛', 'チ゛', 'ツ゛', 'テ゛', 'ト゛', 'ハ゛', 'ヒ゛', 'フ゛', 'ヘ゛', 'ホ゛']
handakuten = ['は゜', 'ひ゜', 'ふ゜', 'へ゜', 'ほ゜', 'ハ゜', 'ヒ゜', 'フ゜', 'ヘ゜', 'ホ゜']

## 正規表現でやろうとすると、一個ずつ書くしかない。濁点と別体のときのコードと濁点と合体したあとのコードに規則性があるのならそれを利用したい。
import re
text = "た゛るまさんか゛"
bytes_text = text.encode('cp932')
print(bytes_text)
text = re.sub("か゛","が",text)
text = re.sub("た゛","だ",text)
print(text)

print("-------------")

## 別解
import unicodedata
a = unicodedata.normalize("NFC", "だるま").encode()
b = unicodedata.normalize("NFD", "だるま").encode()
print(a)
print(b)

#unicodedata.normalize("NFC", text).encode('cp932')
#bytes_text = 

## いままでの書き方
# before = 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ'
# after = 'がぎぐげござじずぜぞだぢづでどばびぶべぼガギグゲゴザジズゼゾダヂヅデドバビブベボ'
# dakuten = []
# for b, a in zip(before, after):
#     bcode = b.encode('cp932') + '゛'.encode('cp932')
#     acode = a.encode('cp932')
#     print(f"{b}゛,{a},{bcode},{acode}")
#     dakuten.append((bcode, acode))
# def fix(self, text):
#     text = text.encode('cp932')
#     for b, a in self.tr_table:
#         text = re.sub(b, a, text)
#     return text.decode('cp932')
