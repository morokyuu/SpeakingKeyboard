#!/bin/python
# pyenv anaconda3
#
# kana-dict.txtを読み込んでmp3を作成する。gttsはオンライン必要。
from gtts import gTTS
import sys
import glob
import re

#msg = "のばしぼう"
#output = gTTS(text=msg,lang='ja',slow=False)
#output.save(f'{msg}.mp3')

msg = "ちいさい つ"
output = gTTS(text=msg,lang='ja',slow=False)
output.save(f'{msg}.mp3')
