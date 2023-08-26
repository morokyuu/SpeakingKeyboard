import keyboard as key
import time
import re

## keyboard input lib
## https://dntf.hatenablog.com/entry/py_keyboard_lib


class DakutenFixer:
    # result = re.sub(b'\x82\xcd\x81K', b'\x82\xcf', code)
    def __init__(self):
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
        self.tr_table = dakuten + handakuten
        
    def fix(self,text):
        text = text.encode('cp932')
        for b, a in self.tr_table:
            text = re.sub(b, a, text)
        return text.decode('cp932')


class JpDecoder:
    # 入力キーをローマ字に置き換える
    def __init__(self):
        self.kana = {'0': "wa", '1': "nu", '2': "hu", '3': "a", '4': "u", '5': "e", '6': "o", '7': "ya", '8': "yu",
                     '9': "yo", 'a': "ti", 'b': "ko", 'c': "so", 'd': "si", 'e': "i", 'f': "ha", 'g': "ki", 'h': "ku",
                     'i': "ni", 'j': "ma", 'k': "no", 'l': "ri", 'm': "mo", 'n': "mi", 'o': "ra", 'p': "se", 'q': "ta",
                     'r': "su", 's': "to", 't': "ka", 'u': "na", 'v': "hi", 'w': "te", 'x': "sa", 'y': "nn", 'z': "tu",
                     ',': "ne", '-': "ho", '.': "ru", '/': "me", ':': "ke", ';': "re", ']': "mu", '^': "he",
                     '\\': "ro", '@':":", '[':'0'}
        self.sokuon_youon= {'z':"xtu",'7':"xya",'8':"xyu",'9':"xyo"}

        self.kana_label = {
            'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
            'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
            'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ねasdf", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
            'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
            'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
            '0':"゜",':':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ"
        }

    def inkey2midkey(self,inkey):
        try:
            midkey = self.kana[inkey]
            return True,midkey
        except:
            pass
        return False,''

    def midkey2label(self,midkey):
        try:
            label = self.kana_label[midkey]
            return True,label
        except:
            pass
        return False,''


class KanaWord:
    def __init__(self):
        with open("kana-dict.txt","r") as fp:
            self.words = [l.rstrip() for l in fp.readlines()]
    def match(self,text):
        pat = re.compile(text)
        for w in self.words:
            if re.match(pat,w):
                print(w)


def mainloop():
    decoder = JpDecoder()
    df = DakutenFixer()
    
    kw = KanaWord()

    spell = ""
    while True:
        inkey = key.read_key()
        time.sleep(0.3)
        if inkey == 'esc':
            exit()

        flag,midkey = decoder.inkey2midkey(inkey)
        if flag:
            print(f"pressed:{midkey}")
            flag,label = decoder.midkey2label(midkey)

            if flag:
                spell += label
                print(f"spell:{spell}")
                spell = df.fix(spell)
                print(f"spell:{spell}")
                kw.match(spell)



if __name__ == '__main__':
    mainloop()
