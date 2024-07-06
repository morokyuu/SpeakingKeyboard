# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 22:19:32 2024

@author: square
"""

class DakutenHandler:
    def __init__(self):
        ## dictitionary creation
        ## https://note.nkmk.me/python-dict-create/
        self.before_daku = 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ'
        self.after_daku  = 'がぎぐげござじずぜぞだぢづでどばびぶべぼガギグゲゴザジズゼゾダヂヅデドバビブベボ'
        self.before_handaku = 'はひふへほハヒフヘホ'
        self.after_handaku  = 'ぱぴぷぺぽパピプペポ'
        
        self.replace_daku    = dict(zip(self.before_daku,self.after_daku))
        self.replace_handaku = dict(zip(self.before_handaku,self.after_handaku))
        self.candidate = self.before_daku + self.before_handaku
        
    # 濁点・半濁点に対応していない文字はそのまま素通りする
    def do(self,spell):
        
        if len(spell)>1:
            new_input = spell[-1]
            last_moji = spell[-2]
            
            if new_input in '゛':
                if last_moji in self.candidate:
                    spell = spell[:-2] + self.replace_daku[last_moji]
            
            elif new_input in '゜':
                if last_moji in self.candidate:
                    spell = spell[:-2] + self.replace_handaku[last_moji]
        else:
            pass
        
        return spell


dkt_handler = DakutenHandler()

## ------------------
print(f'test1')

spell = "ころんた゛"

modified = dkt_handler.do(spell)
print(f'{modified}')

## ------------------
print(f'test2')

spell = "はっは゜"

modified = dkt_handler.do(spell)
print(f'{modified}')

## ------------------
print(f'test3')

spell = "しお゜"

modified = dkt_handler.do(spell)
print(f'{modified}')

## ------------------
print(f'test4')

spell = "゜"

modified = dkt_handler.do(spell)
print(f'{modified}')

## ------------------
print(f'test5')

spell = "゛゛゜"

modified = dkt_handler.do(spell)
print(f'{modified}')

## ------------------
print(f'test6')

spell = " ゜"

modified = dkt_handler.do(spell)
print(f'{modified}')

