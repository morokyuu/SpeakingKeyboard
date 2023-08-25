import keyboard as key
import time

## keyboard input lib
## https://dntf.hatenablog.com/entry/py_keyboard_lib

class JpDecoder:
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

    def loop(self):
        spell = ""
        while True:
            inkey = key.read_key()
            time.sleep(0.3)
            if inkey == 'esc':
                exit()

            flag,midkey = self.inkey2midkey(inkey)
            if flag:
                print(f"pressed:{midkey}")
                flag,label = self.midkey2label(midkey)

                if flag:
                    spell += label
                print(f"spell:{spell}")
                code = spell.encode('cp932')
                print(f"code:{code}")


if __name__ == '__main__':
    decoder = JpDecoder()
    decoder.loop()
