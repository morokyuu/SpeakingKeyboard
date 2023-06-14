# This is a sample Python script.
import string

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pygame.locals import *
import pygame
import sys
import os
import time
import glob
from enum import Enum

GREEN = (0, 255, 0)
BLUE = (0, 0, 123)
WHITE = (255, 255, 255)

class AlphabetFont:
    def __init__(self,char="hello"):
        self.fontObj = pygame.font.Font('freesansbold.ttf', 130)
        self.charSurfaceObj = self.fontObj.render(char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def change(self,char):
        if len(char) == 1:
            if char.islower():
                char = char.upper()
            char = " " + char + " "

        self.charSurfaceObj = self.fontObj.render(char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def blit(self):
        DISPLAYSURF.blit(self.charSurfaceObj, self.charRectObj)


class KanaFont:
    def __init__(self,char="kana mode"):
        self.fontObj = pygame.font.Font('freesansbold.ttf', 130)
        self.charSurfaceObj = self.fontObj.render(char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

        self.kana_img = pygame.image.load("./font/kana_font.png").convert_alpha()
        self.kana_dict,self.num_dict = load_kana_dict()
        self.kana_num = 0

    def change(self,char):
        #print(f"{char} {type(char)} {len(char)}")
        if len(char) == 1:
            try:
                if char == '\\':
                    play_effect_kotsu()
                    self.kana_num = -1
                else:
                    self.kana_num = int(self.num_dict[char])
            except:
                self.kana_num = -1
        elif len(char) > 1:
            play_effect_kotsu()
            self.kana_num = -1
        # len of char of RO-key is zero.
        elif len(char) == 0:
            self.kana_num = int(self.num_dict['\\'])

    def blit(self):
        if self.kana_num < 0:
            pass
        else:
            DISPLAYSURF.blit(self.kana_img,(300,300),pygame.Rect(0,int(self.kana_num)*70,70,70))


class FontDisplay:
    def __init__(self):
        self.mode = Mode.ENGLISH
        self.font_gen = AlphabetFont()

    def change(self,char,mode):
        self.char = char
        self.mode = mode

        if self.mode == Mode.ENGLISH:
            self.font_gen = AlphabetFont()
        elif self.mode == Mode.JAPANESE:
            self.font_gen = KanaFont()
        self.font_gen.change(char)

    def draw(self):
        self.font_gen.blit()


class Mode(Enum):
    ENGLISH = 0,
    JAPANESE = 1


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


def play_effect_kotsu():
    sound = pygame.mixer.Sound("./wav/effect/kotsu.mp3")
    sound.play()

def play_effect_picon():
    sound = pygame.mixer.Sound("./wav/effect/picon.mp3")
    sound.play()

class SoundPlayer:
    def __init__(self):
        self.mp3dict = load_eng_dict()
        #load_kana_dict()

    def set_mode(self,mode):
        if mode == Mode.ENGLISH:
            self.mp3dict = load_eng_dict()
        elif mode == Mode.JAPANESE:
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


class Jp_SpellingObserver:
    def __init__(self):
        #self.kana_spell = [["na","su"],["a","sa","ga","o"]]
        self.kana_spell = ["nasu","asagao","tikatetu"]
        self.queue = []

    def _check(self,queue):
        for sp in self.kana_spell:
            if sp in queue:
                self.queue.clear()
                return True,sp
        return False,None

    def input(self,key_obj):
        self.queue.append(key_obj)
        q = [k.raw for k in self.queue]
        q = ''.join(q)
        print(q)

        l = [k.label for k in self.queue]
        l = ''.join(l)
        print(l)

        exist,val = self._check(q)
        if exist:
            print("spell found------------")
            val = KeyObj(val,l)
            return val
        else:
            return key_obj

class Eng_SpellingObserver:
    def __init__(self):
        self.queue = []
        self.spell = {"abc","hello","pig","money","book"}


    def _check(self,q):
        for sp in self.spell:
            if sp in q:
                self.queue.clear()
                return True,sp
        return False,None

    def input(self,key_obj):
        self.queue.append(key_obj)
        q = [k.raw for k in self.queue]
        q = ''.join(q)
        exist,val = self._check(q)
        if exist:
            print("spell found------------")
            val = KeyObj(val,val)
            return val
        else:
            return key_obj






class KeyObj:
    def __init__(self,raw,label):
        self.raw = raw
        self.label = label

class JpDecoder:
    def __init__(self):
        self.kana = {'0': "wa", '1': "nu", '2': "hu", '3': "a", '4': "u", '5': "e", '6': "o", '7': "ya", '8': "yu",
                     '9': "yo", 'a': "ti", 'b': "ko", 'c': "so", 'd': "si", 'e': "i", 'f': "ha", 'g': "ki", 'h': "ku",
                     'i': "ni", 'j': "ma", 'k': "no", 'l': "ri", 'm': "mo", 'n': "mi", 'o': "ra", 'p': "se", 'q': "ta",
                     'r': "su", 's': "to", 't': "ka", 'u': "na", 'v': "hi", 'w': "te", 'x': "sa", 'y': "nn", 'z': "tu",
                     ',': "ne", '-': "ho", '.': "ru", '/': "me", ':': "ke", ';': "re", ']': "mu", '^': "he",
                     '\\': "ro", }
        self.hatsuon = {'[':"maru",'@':"dakuten",'z':"xtu",'7':"xya",'8':"xyu",'9':"xyo"}

        self.kana_label = {
            'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
            'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
            'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ね", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
            'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
            'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
            'maru':"゜",'dakuten':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ"
        }

    def _exchange(self,keyname,shift):
        if not "shift" in keyname and shift == True:
            try:
                val = self.hatsuon[keyname]
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
        val = self._exchange(keyname,shift)
        label = self._get_label(val)
        return KeyObj(val,label)

class EngDecoder:
    def __init__(self):
        pass

    def do(self,keyname,shift=False):
        return KeyObj(keyname,keyname)




class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        self.sp = SoundPlayer()
        play_effect_picon()

        self.fontd = FontDisplay()
        self.mode = Mode.ENGLISH

        self.key_decoder = EngDecoder()
        self.spo = Eng_SpellingObserver()

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
        if self.mode == Mode.ENGLISH:
            self.mode = Mode.JAPANESE
            self.key_decoder = JpDecoder()
            self.spo = Jp_SpellingObserver()
        elif self.mode == Mode.JAPANESE:
            self.mode = Mode.ENGLISH
            self.key_decoder = EngDecoder()
            self.spo = Eng_SpellingObserver()
        self.sp.set_mode(self.mode)

    def do(self):
        while True:
            DISPLAYSURF.fill(WHITE)
            pygame.draw.polygon(DISPLAYSURF, GREEN,
                                ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
                                )
            DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)

            key_obj = KeyObj("","")
            keyname,shift = self.input_key()

            if keyname is None:
                pass
            else:
                if keyname == 'space':
                    print("mode change")
                    self.change_mode()
                else:
                    key_obj = self.key_decoder.do(keyname, shift)

                    self.sp.play(keyname)
                    self.fontd.change(keyname,self.mode)

            if len(key_obj.raw) > 0:
                key_obj = self.spo.input(key_obj)
                print(key_obj.raw)

            self.fontd.draw()
            pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    flags = pygame.FULLSCREEN
    #DISPLAYSURF = pygame.display.set_mode(size=(640,480), display=0, depth=32, flags=pygame.FULLSCREEN)
    DISPLAYSURF = pygame.display.set_mode(size=(640,480), display=0, depth=32)
    pygame.display.set_caption('Hit any key')

    g = GameLoop()
    while True:
        g.do()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
