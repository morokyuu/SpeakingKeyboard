#!/bin/python
# pyenv anaconda3
#
# kana-dict.txtを読み込んでmp3を作成する。gttsはオンライン必要。
# 単語リストはshiftjis-CRLFで作成する。
from gtts import gTTS
import sys

with open("../../kana-dict.txt",encoding='shift_jis') as fp:
    lines = fp.readlines()
    lines = [line.rstrip() for line in lines]

print(lines)

for msg in lines:
    output = gTTS(text=msg,lang='ja',slow=False)
    output.save(f'{msg}.mp3')

