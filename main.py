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
                self.kana_num = int(self.num_dict[char])
            except:
                self.kana_num = -1
        # len of char of RO-key is zero.
        elif len(char) == 0:
            self.kana_num = int(self.num_dict['\\'])

    def blit(self):
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
        elif self.mode == Mode.KANA:
            self.font_gen = KanaFont()
        self.font_gen.change(char)

    def draw(self):
        self.font_gen.blit()


class Mode(Enum):
    ENGLISH = 0,
    KANA = 1


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

class SoundPlayer:
    def __init__(self):
        self.mp3dict = load_eng_dict()
        #load_kana_dict()

    def set_mode(self,mode):
        if mode == Mode.ENGLISH:
            self.mp3dict = load_eng_dict()
        elif mode == Mode.KANA:
            self.mp3dict,_ = load_kana_dict()
        pass

    def play_effect_kotsu(self):
        sound = pygame.mixer.Sound("./wav/effect/kotsu.mp3")
        sound.play()

    def play_effect_picon(self):
        sound = pygame.mixer.Sound("./wav/effect/picon.mp3")
        sound.play()

    def play(self,name):
        path = ""
        try:
            # len of char of RO-key is zero.
            if len(name) == 0:
                path = self.mp3dict['\\']
            elif len(name) == 1 and name == '\\':
                self.play_effect_kotsu()
            else:
                path = self.mp3dict[name]
            sound = pygame.mixer.Sound(path)
            sound.play()
        except:
            self.play_effect_kotsu()



class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        self.sp = SoundPlayer()
        self.sp.play_effect_picon()

        self.fontd = FontDisplay()
        self.mode = Mode.ENGLISH

    def input_key(self) -> str | None:
        keyname = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    keyname = pygame.key.name(event.key)
        return keyname

    def change_mode(self):
        if self.mode == Mode.ENGLISH:
            self.mode = Mode.KANA
        elif self.mode == Mode.KANA:
            self.mode = Mode.ENGLISH
        self.sp.set_mode(self.mode)

    def do(self):
        while True:
            DISPLAYSURF.fill(WHITE)
            pygame.draw.polygon(DISPLAYSURF, GREEN,
                                ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
                                )
            DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)

            keyname = self.input_key()
            if keyname is None:
                pass
            else:
                if keyname == 'space':
                    print("mode change")
                    self.change_mode()
                else:
                    print(keyname)
                    self.sp.play(keyname)
                    self.fontd.change(keyname,self.mode)

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
