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
import sqlite3

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

    def clear(self):
        self.charSurfaceObj = self.font.render(f"< >", True, GREEN, BLUE)
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
    def play(self,romaji,mode):
        path = ""
        if mode == mode.HIRAGANA or mode == mode.KATAKANA:
            romaji = romaji.upper()
            path = f"wav//hiragana//{romaji}.mp3"
        else:
            path = f"wav//english//{romaji}.mp3"
        print(path)

        try:
            sound = pygame.mixer.Sound(path)
            sound.play()
        except FileNotFoundError:
            play_effect_kotsu()

class WordDict2:
    def __init__(self):
        dbname = 'tango.db'
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def close(self):
        print("WordDict close")
        self.conn.close()

    def get_candidate(self, text, mode):
        if mode.KATAKANA == mode:
            ## todo katakana henkan
            targ = (f"{text}%",)
            print(targ)
            self.cur.execute("""
                select * from words
                inner join katakana
                on words.id = katakana.id
                where words.word like ? and katanaka.has_katakana = 1
                """,targ)
            for row in self.cur:
                print(row)
        else:
            targ = (f"{text}%",)
            print(targ)
            self.cur.execute("select * from words where word like ?",targ)
            for row in self.cur:
                print(row)
        candidate = []
        fullmatch = ""
        return candidate, fullmatch

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


class DakutenFilter:
    def __init__(self):
        ## dictitionary creation
        ## https://note.nkmk.me/python-dict-create/
        self.before_daku = 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ'
        self.after_daku = 'がぎぐげござじずぜぞだぢづでどばびぶべぼガギグゲゴザジズゼゾダヂヅデドバビブベボ'
        self.before_handaku = 'はひふへほハヒフヘホ'
        self.after_handaku = 'ぱぴぷぺぽパピプペポ'

        self.replace_daku = dict(zip(self.before_daku, self.after_daku))
        self.replace_handaku = dict(zip(self.before_handaku, self.after_handaku))

    # 濁点・半濁点に対応していない文字はそのまま素通りする
    def do(self, spell):

        if len(spell) > 1:
            new_input = spell[-1]
            last_moji = spell[-2]

            if new_input in '゛':
                if last_moji in self.before_daku:
                    spell = spell[:-2] + self.replace_daku[last_moji]

            elif new_input in '゜':
                if last_moji in self.before_handaku:
                    spell = spell[:-2] + self.replace_handaku[last_moji]
        else:
            pass

        return spell

class SpellBuffer:
    def __init__(self):
        self.spell = ""
        self.dakuten = DakutenFilter()

    def clear(self):
        self.spell = ""

    def put(self,moji):
        self.spell = self.spell + moji
        self.spell = self.dakuten.do(self.spell)

    def get(self):
        return self.spell

class KeynameDecoder:
    def __init__(self):
        # 仮名漢字入力モードの時に使う仮名キーの刻印に対応したローマ字読みに変換する
        self.kana = {'0': "wa", '1': "nu", '2': "hu", '3': "a", '4': "u", '5': "e", '6': "o", '7': "ya", '8': "yu",
                     '9': "yo", 'a': "ti", 'b': "ko", 'c': "so", 'd': "si", 'e': "i", 'f': "ha", 'g': "ki", 'h': "ku",
                     'i': "ni", 'j': "ma", 'k': "no", 'l': "ri", 'm': "mo", 'n': "mi", 'o': "ra", 'p': "se", 'q': "ta",
                     'r': "su", 's': "to", 't': "ka", 'u': "na", 'v': "hi", 'w': "te", 'x': "sa", 'y': "nn", 'z': "tu",
                     ',': "ne", '-': "ho", '.': "ru", '/': "me", ':': "ke", ';': "re", ']': "mu", '^': "he",
                     '\\': "ro", '@': ":", '[': '0'}
        self.sokuon_youon_nobashi= {'z':"xtu",'7':"xya",'8':"xyu",'9':"xyo",'-':"nobashi"}

        self.hiragana_label = {
            'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
            'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
            'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ね", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
            'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
            'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
            '0':"゜",':':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ",'nobashi':"ー"
        }
        self.katakana_label = {
            'a': "ア", 'i': "イ", 'u': "ウ", 'e': "エ", 'o': "オ", 'ka': "カ", 'ki': "キ", 'ku': "ク", 'ke': "ケ", 'ko': "コ",
            'sa': "サ", 'si': "シ", 'su': "ス", 'se': "セ", 'so': "ソ", 'ta': "タ", 'ti': "チ", 'tu': "ツ", 'te': "テ",
            'to': "ト", 'na': "ナ", 'ni': "ニ", 'nu': "ヌ", 'ne': "ネ", 'no': "ノ", 'ha': "ハ", 'hi': "ヒ", 'hu': "フ",
            'he': "ヘ", 'ho': "ホ", 'ma': "マ", 'mi': "ミ", 'mu': "ム", 'me': "メ", 'mo': "モ", 'ya': "ヤ", 'yu': "ユ",
            'yo': "ヨ", 'ra': "ラ", 'ri': "リ", 'ru': "ル", 're': "レ", 'ro': "ロ", 'wa': "ワ", 'wo': "ヲ", 'nn': "ン",
            '0':"゜",':':"゛",'xtu':"ッ",'xya':"ャ",'xyu':"ュ",'xyo':"ョ",'nobashi':"ー"
        }

    def keyname2romaji(self,keyname,shift):
        ## shift key
        if not "shift" in keyname and shift == True:
            #print(f'keyname={keyname} shift={shift}')
            ## with shift key (keyname='left shift' or 'right shift')
            try:
                val = self.sokuon_youon_nobashi[keyname]
            except:
                val = ""
        else:
            ## without shift key
            try:
                val = self.kana[keyname]
            except:
                val = ""
        return val

    def romaji2label(self,romaji,label_dict):
        ## label
        try:
            label = label_dict[romaji]
        except:
            label = ""
        return label

    def do(self,keyname,shift=False,mode=Mode.ENGLISH):
        romaji = ""
        label = ""

        if mode==Mode.ENGLISH:
            ## labelは小文字のままとし、表示するときに大文字小文字を好みで変更することにした
            if keyname in string.ascii_letters + string.digits:
                label = keyname
                romaji = keyname
        elif mode == Mode.HIRAGANA or mode == Mode.KATAKANA:
            romaji = self.keyname2romaji(keyname, shift)
            if mode==Mode.HIRAGANA:
                label = self.romaji2label(romaji,self.hiragana_label)
            elif mode==Mode.KATAKANA:
                label = self.romaji2label(romaji,self.katakana_label)
        return romaji,label

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


        self.mode = Mode.HIRAGANA
        self.knd = KeynameDecoder()

        self.spellbuf = SpellBuffer()


        self.wd = WordDict2()
        self.sp = MojiSoundPlayer()

        print(self.mode)


    def _halt(self):
        self.wd.close()
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
        elif self.mode == Mode.KATAKANA:
            self.mode = Mode.ENGLISH
        elif self.mode == Mode.ENGLISH:
            self.mode = Mode.HIRAGANA
        #self.sp.set_mode(self.mode)
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
            self.spellbuf.clear()
        # return-key to reset spell
        elif keyname == 'return':
            print("========return")
            self.spellbuf.clear()
            self.fontd.change("  ")
            self.spelld.clear()
            self.candidated.change([])

            if self.fullmatch:
                print(f'===fullmatch {self.fullmatch} ===')
                play_word(self.fullmatch)
                play_effect_pinpon()
                self.fullmatch = None
        else:
            romaji,label = self.knd.do(keyname, shift, self.mode)
            self.spellbuf.put(label)

            print(f"romaji={romaji}, label={label}, spellbuf={self.spellbuf.get()}")

            self.sp.play(romaji,self.mode)
            self.fontd.change(label)
            self.spelld.change(self.spellbuf.get())

            candidate, self.fullmatch = self.wd.get_candidate(self.spellbuf.get(), self.mode)
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
