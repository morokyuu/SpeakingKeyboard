##
## required version
##   python 3.10
##   pygame 2.4.0
##
from pygame.locals import *
import pygame
import sys
import os
import time
import glob
from enum import Enum
import re
import random
import string

FULLSCREEN_MODE = False

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 123)
WHITE = (255, 255, 255)

WINDOWSIZE = (640,480)


class Display:
    def __init__(self,char="こんにちは"):
        self.font = pygame.font.SysFont('yugothicuisemibold', 70)
        self.charSurfaceObj = self.font.render(char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def draw(self):
        DISPLAYSURF.blit(self.charSurfaceObj,self.charRectObj)


class FontDisplay(Display):
    def __init__(self):
        super().__init__()

    def change(self,char):
        if len(char) > 0 and char[0] in string.ascii_lowercase:
            char = char.upper()
        self.charSurfaceObj = self.font.render(f"{char}", True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

class SpellDisplay(Display):
    def __init__(self):
        super().__init__()

    def change(self,char):
        self.charSurfaceObj = self.font.render(f"<{char}>", True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 380)

class CandidateDisplay():
    def __init__(self):
        self.cand_surflist = []

    def setOneCandidate(self,candidate):
        self.font = pygame.font.SysFont('yugothicuisemibold', 100)
        fontsurf = self.font.render(f"{candidate[0]}", True, BLACK)
        charRectObj = fontsurf.get_rect()
        charRectObj.center = (WINDOWSIZE[0]/2,70)
        self.cand_surflist.append((fontsurf, charRectObj))

    def setSomeCandidate(self,candidate):
        fontsize = int(80 * 1/len(candidate))
        L,H = (10,WINDOWSIZE[0]-10)

        randx = [random.randrange(L,H) for _ in range(len(candidate))]
        self.font = pygame.font.SysFont('yugothicuisemibold', fontsize)

        for i,c in enumerate(candidate):
            x = randx[i]
            fontsurf = self.font.render(f"{c}", True, BLACK)
            charRectObj = fontsurf.get_rect()
            charRectObj.center = (x, 20+i*13)
            self.cand_surflist.append((fontsurf,charRectObj))

    def change(self,candidate):
        self.cand_surflist.clear()
        if len(candidate) >= 2:
            self.setSomeCandidate(candidate)
        elif len(candidate) == 1:
            self.setOneCandidate(candidate)
        else:
            return



    def draw(self):
        for surf,rect in self.cand_surflist:
            DISPLAYSURF.blit(surf,rect)


class Mode(Enum):
    ENGLISH = 0,
    HIRAGANA = 1,
    KATAKANA = 2

def load_eng_dict():
    with open("eng_mode","r") as fp:
        lines = [line.rstrip() for line in fp.readlines()]
    char_dict = {}
    for line in lines:
        col = line.split(' ')
        assert len(col) == 3,"file: num of column error."
        char_dict[col[0]] = col[2]
    return char_dict

def load_kana_dict():
    with open("kana_mode","r") as fp:
        lines = [line.rstrip() for line in fp.readlines()]
    char_dict = {}
    num_dict = {}
    for line in lines:
        col = line.split(' ')
        assert len(col) == 4,"file: num of column error."
        char_dict[col[0]] = col[2]
        num_dict[col[0]] = col[3]
    return char_dict,num_dict


def play_effect_modechange(mode):
    if mode == Mode.HIRAGANA:
        sound = pygame.mixer.Sound("./wav/effect/an-nihongo-mode.mp3")
        sound.play()
    elif mode == Mode.ENGLISH:
        sound = pygame.mixer.Sound("./wav/effect/an-english-mode.mp3")
        sound.play()

def play_effect_kotsu():
    sound = pygame.mixer.Sound("./wav/effect/kotsu.mp3")
    sound.play()

def play_effect_picon():
    sound = pygame.mixer.Sound("./wav/effect/picon.mp3")
    sound.play()

def play_word(word):
    try:
        sound = pygame.mixer.Sound(f"./wav/kana-words/{word}.mp3")
        sound.play()
        for _ in range(100):
            time.sleep(0.05)
            if not pygame.mixer.get_busy():
                break
    except:
        pass

def play_effect_pinpon():
    sound = pygame.mixer.Sound("./wav/effect/pinpon.mp3")
    sound.play()


class MojiSoundPlayer:
    def __init__(self):
        pass

    def set_mode(self,mode):
        if mode == Mode.ENGLISH:
            self.mp3dict = load_eng_dict()
        elif mode == Mode.HIRAGANA:
            self.mp3dict,_ = load_kana_dict()
        pass

    def play(self,name):
        path = ""
        try:
            # len of char of RO-key is zero.
            if len(name) == 0:
                path = self.mp3dict['\\']
            elif len(name) == 1 and name == '\\':
                play_effect_kotsu()
            else:
                path = self.mp3dict[name]
            sound = pygame.mixer.Sound(path)
            sound.play()
        except:
            play_effect_kotsu()


class WordDict:
    def __init__(self,dict_filepath):
        self.words = []
        with open(dict_filepath, "r") as fp:
            self.words = [l.rstrip() for l in fp.readlines()]

    def get_candidate(self, text):
        candidate = []
        fullmatch = ""
        pat = re.compile(text)
        for w in self.words:
            if re.match(pat, w):
                candidate.append(w)
            if re.fullmatch(pat, w):
                fullmatch = w
        return candidate, fullmatch

class KanaWordDict(WordDict):
    def __init__(self):
        super().__init__("kana-dict.txt")

class EngWordDict(WordDict):
    def __init__(self):
        super().__init__("eng-dict.txt")





class KeynameDecoder:
    def __init__(self):
        self.kana = {'0': "wa", '1': "nu", '2': "hu", '3': "a", '4': "u", '5': "e", '6': "o", '7': "ya", '8': "yu",
                     '9': "yo", 'a': "ti", 'b': "ko", 'c': "so", 'd': "si", 'e': "i", 'f': "ha", 'g': "ki", 'h': "ku",
                     'i': "ni", 'j': "ma", 'k': "no", 'l': "ri", 'm': "mo", 'n': "mi", 'o': "ra", 'p': "se", 'q': "ta",
                     'r': "su", 's': "to", 't': "ka", 'u': "na", 'v': "hi", 'w': "te", 'x': "sa", 'y': "nn", 'z': "tu",
                     ',': "ne", '-': "ho", '.': "ru", '/': "me", ':': "ke", ';': "re", ']': "mu", '^': "he",
                     '\\': "ro", '@': ":", '[': '0'}
        self.sokuon_youon= {'z':"xtu",'7':"xya",'8':"xyu",'9':"xyo"}

        self.hiragana_label = {
            'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
            'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
            'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ね", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
            'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
            'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
            '0':"゜",':':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ"
        }
        self.katakana_label = {
            'a': "ア", 'i': "イ", 'u': "ウ", 'e': "エ", 'o': "オ", 'ka': "カ", 'ki': "キ", 'ku': "ク", 'ke': "ケ", 'ko': "コ",
            'sa': "サ", 'si': "シ", 'su': "ス", 'se': "セ", 'so': "ソ", 'ta': "タ", 'ti': "チ", 'tu': "ツ", 'te': "テ",
            'to': "ト", 'na': "ナ", 'ni': "ニ", 'nu': "ヌ", 'ne': "ネ", 'no': "ノ", 'ha': "ハ", 'hi': "ヒ", 'hu': "フ",
            'he': "ヘ", 'ho': "ホ", 'ma': "マ", 'mi': "ミ", 'mu': "ム", 'me': "メ", 'mo': "モ", 'ya': "ヤ", 'yu': "ユ",
            'yo': "ヨ", 'ra': "ラ", 'ri': "リ", 'ru': "ル", 're': "レ", 'ro': "ロ", 'wa': "ワ", 'wo': "ヲ", 'nn': "ン",
            '0':"゜",':':"゛",'xtu':"ッ",'xya':"ャ",'xyu':"ュ",'xyo':"ョ"
        }

    def decode_kana(self,keyname,shift,label_dict):
        ## shift key
        if not "shift" in keyname and shift == True:
            ## with shift key
            try:
                val = self.sokuon_youon[keyname]
            except:
                val = ""
        else:
            ## without whift key
            try:
                val = self.kana[keyname]
            except:
                val = ""
        ## label
        try:
            label = label_dict[val]
        except:
            label = ""
        return label

    def do(self,keyname,shift=False,mode=Mode.ENGLISH):
        if mode==Mode.HIRAGANA:
            label = self.decode_kana(keyname,shift,self.hiragana_label)
        elif mode==Mode.KATAKANA:
            label = self.decode_kana(keyname,shift,self.katakana_label)
        else:
            label = keyname
        return label

class JpDecoder:
    def __init__(self,mode = Mode.HIRAGANA):
        self.kana = {'0': "wa", '1': "nu", '2': "hu", '3': "a", '4': "u", '5': "e", '6': "o", '7': "ya", '8': "yu",
                     '9': "yo", 'a': "ti", 'b': "ko", 'c': "so", 'd': "si", 'e': "i", 'f': "ha", 'g': "ki", 'h': "ku",
                     'i': "ni", 'j': "ma", 'k': "no", 'l': "ri", 'm': "mo", 'n': "mi", 'o': "ra", 'p': "se", 'q': "ta",
                     'r': "su", 's': "to", 't': "ka", 'u': "na", 'v': "hi", 'w': "te", 'x': "sa", 'y': "nn", 'z': "tu",
                     ',': "ne", '-': "ho", '.': "ru", '/': "me", ':': "ke", ';': "re", ']': "mu", '^': "he",
                     '\\': "ro", '@': ":", '[': '0'}
        self.sokuon_youon= {'z':"xtu",'7':"xya",'8':"xyu",'9':"xyo"}

        if Mode.HIRAGANA == mode:
            self.kana_label = {
                'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
                'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
                'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ね", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
                'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
                'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
                '0':"゜",':':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ"
            }
        elif Mode.KATAKANA == mode:
            self.kana_label = {
                'a': "ア", 'i': "イ", 'u': "ウ", 'e': "エ", 'o': "オ", 'ka': "カ", 'ki': "キ", 'ku': "ク", 'ke': "ケ", 'ko': "コ",
                'sa': "サ", 'si': "シ", 'su': "ス", 'se': "セ", 'so': "ソ", 'ta': "タ", 'ti': "チ", 'tu': "ツ", 'te': "テ",
                'to': "ト", 'na': "ナ", 'ni': "ニ", 'nu': "ヌ", 'ne': "ネ", 'no': "ノ", 'ha': "ハ", 'hi': "ヒ", 'hu': "フ",
                'he': "ヘ", 'ho': "ホ", 'ma': "マ", 'mi': "ミ", 'mu': "ム", 'me': "メ", 'mo': "モ", 'ya': "ヤ", 'yu': "ユ",
                'yo': "ヨ", 'ra': "ラ", 'ri': "リ", 'ru': "ル", 're': "レ", 'ro': "ロ", 'wa': "ワ", 'wo': "ヲ", 'nn': "ン",
                '0':"゜",':':"゛",'xtu':"ッ",'xya':"ャ",'xyu':"ュ",'xyo':"ョ"
            }

    def _exchange(self,keyname,shift):
        if not "shift" in keyname and shift == True:
            try:
                val = self.sokuon_youon[keyname]
            except:
                val = ""
        else:
            try:
                val = self.kana[keyname]
            except:
                val = ""
        return val

    def _get_label(self,val):
        try:
            label = self.kana_label[val]
        except:
            label = ""
        return label

    def do(self,keyname,shift=False):
        midkey = self._exchange(keyname,shift)
        label = self._get_label(midkey)
        return label

class EngDecoder:
    def __init__(self):
        pass

    def do(self,char,shift=False):
        return char


class DakutenFixer:
    # result = re.sub(b'\x82\xcd\x81K', b'\x82\xcf', code)
    def __init__(self,mode=Mode.HIRAGANA):
        before = 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ'
        after = 'がぎぐげござじずぜぞだぢづでどばびぶべぼガギグゲゴザジズゼゾダヂヅデドバビブベボ'

        dakuten = []
        for b, a in zip(before, after):
            bcode = b.encode('cp932') + '゛'.encode('cp932')
            acode = a.encode('cp932')
            # print(f"{b}゛,{a},{bcode},{acode}")
            dakuten.append((bcode, acode))

        before = 'はひふへほハヒフヘホ'
        after = 'ぱぴぷぺぽパピプペポ'

        handakuten = []
        for b, a in zip(before, after):
            bcode = b.encode('cp932') + '゜'.encode('cp932')
            acode = a.encode('cp932')
            # print(f"{b}゜,{a},{bcode},{acode}")
            handakuten.append((bcode, acode))
        self.tr_table = dakuten + handakuten

    def fix(self, text):
        text = text.encode('cp932')
        for b, a in self.tr_table:
            text = re.sub(b, a, text)
        return text.decode('cp932')


class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        play_effect_picon()

        self.fontd = FontDisplay()
        self.spelld = SpellDisplay()
        self.candidated = CandidateDisplay()

        self.dakutenf = DakutenFixer()

        self.mode = Mode.HIRAGANA
        self.key_decoder = JpDecoder()
        self.wd = KanaWordDict()

        self.sp = MojiSoundPlayer()
        self.sp.set_mode(self.mode)

        print(self.mode)

        self.spell = ""

    def _halt(self):
        pygame.quit()
        sys.exit()

    def input_key(self):
        keyname = None
        shift = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._halt()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._halt()
                else:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        shift = True
                    keyname = pygame.key.name(event.key)
        return keyname,shift

    def change_mode(self):
        if self.mode == Mode.HIRAGANA:
            self.mode = Mode.KATAKANA
            self.key_decoder = JpDecoder(Mode.KATAKANA)
            self.wd = KanaWordDict()
        elif self.mode == Mode.KATAKANA:
            self.mode = Mode.ENGLISH
            self.key_decoder = EngDecoder()
            self.wd = EngWordDict()
        elif self.mode == Mode.ENGLISH:
            self.mode = Mode.HIRAGANA
            self.key_decoder = JpDecoder(Mode.HIRAGANA)
            self.wd = KanaWordDict()
        self.sp.set_mode(self.mode)
        play_effect_modechange(self.mode)

    def do(self):
        DISPLAYSURF.fill(WHITE)
        pygame.draw.polygon(DISPLAYSURF, GREEN,
                            ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
                            )
        DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)
        keyname,shift = self.input_key()

        if keyname is None:
            pass
        elif keyname == 'space':
            print("mode change")
            self.change_mode()
            self.spell = ""
        # return-key to reset spell
        elif keyname == 'return':
            print("========return")
            self.spell = ""
            self.fontd.change("  ")
            self.spelld.change(self.spell)
            self.candidated.change([])

            if self.fullmatch:
                print(f'===fullmatch {self.fullmatch} ===')
                play_word(self.fullmatch)
                play_effect_pinpon()
                self.fullmatch = None
        else:

            # debug
            knd = KeynameDecoder()
            self.mode = Mode.KATAKANA
            label = knd.do(keyname, shift, self.mode)
            print(label)

            return

            label = self.key_decoder.do(keyname, shift)
            self.spell += label
            self.spell = self.dakutenf.fix(self.spell) #gengo izon no bubun ga rosyutushite shimatteiru
            print(f"now = {self.spell}")

            self.sp.play(keyname)
            self.fontd.change(label)
            self.spelld.change(self.spell)

            candidate, self.fullmatch = self.wd.get_candidate(self.spell)
            if len(candidate) > 0:
                for i,c in enumerate(candidate):
                    print(f" candidate[{i}]:{c}")
            self.candidated.change(candidate)
            if self.fullmatch:
                print(f"fullmatch:{self.fullmatch}")

        self.fontd.draw()
        self.spelld.draw()
        self.candidated.draw()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    if FULLSCREEN_MODE:
        DISPLAYSURF = pygame.display.set_mode(size=WINDOWSIZE, display=0, depth=32, flags=pygame.FULLSCREEN)
    else:
        DISPLAYSURF = pygame.display.set_mode(size=WINDOWSIZE, display=0, depth=32)
    pygame.display.set_caption('Speaking Keyboard')

    clock = pygame.time.Clock()


    g = GameLoop()
    while True:
        g.do()
        clock.tick(15)
        pygame.display.flip()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
