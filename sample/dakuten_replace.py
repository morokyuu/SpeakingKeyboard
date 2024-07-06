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
        

    def do(self,new_input,spell):
        try:
            lastmoji = spell[-1]
        except IndexError:
            return spell
        
        print(lastmoji)
        
        if not lastmoji in self.candidate:
            print(f"---the {new_input} is not used to {lastmoji}")
            return spell
        
        elif new_input == '゛':
            try:
                spell = spell[:-1] + self.replace_daku[lastmoji]
            except KeyError:
                pass
        
        elif new_input == '゜':
            try:
                spell = spell[:-1] + self.replace_handaku[lastmoji]
            except KeyError:
                pass
        
        return spell


dkt_handler = DakutenHandler()

## ------------------
print(f'test1')

spell = "ころんた"
new_input = '゛'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

## ------------------
print(f'test2')

spell = "はっは"
new_input = '゜'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

## ------------------
print(f'test3')

spell = "しお"
new_input = '゜'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

## ------------------
print(f'test4')

spell = ""
new_input = '゜'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

## ------------------
print(f'test5')

spell = "゛゛"
new_input = '゜'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

## ------------------
print(f'test6')

spell = " "
new_input = '゜'

modified = dkt_handler.do(new_input,spell)
print(f'{modified}')

