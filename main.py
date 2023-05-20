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



class FontDisplay:
    def __init__(self,char="hello"):
        self.char = char

        self.fontObj = pygame.font.Font('freesansbold.ttf', 130)
        self.charSurfaceObj = self.fontObj.render(self.char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def change(self,char):
        self.char = char
        if len(self.char)==1:
            if self.char.islower():
                self.char = self.char.upper()
            self.char = " " + self.char + " "
        self.charSurfaceObj = self.fontObj.render(self.char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def draw(self):
        DISPLAYSURF.blit(self.charSurfaceObj, self.charRectObj)
        return


class Mode(Enum):
    ENGLISH = 0,
    KANA = 1


class SoundPlayer:
    def __init__(self):
        self.load_eng_dict()
        #self.load_kana_dict()

    def load_eng_dict(self):
        with open("eng_mode","r") as fp:
            lines = [line.rstrip() for line in fp.readlines()]

        self.mp3dict = {}
        for line in lines:
            col = line.split(' ')
            assert len(col) == 3,"file: num of column error."
            self.mp3dict[col[0]] = col[2]

    def load_kana_dict(self):
        with open("kana_mode","r") as fp:
            lines = [line.rstrip() for line in fp.readlines()]

        self.mp3dict = {}
        for line in lines:
            col = line.split(' ')
            assert len(col) == 3,"file: num of column error."
            self.mp3dict[col[0]] = col[2]

    def change_mode(self,mode):
        if mode == Mode.ENGLISH:
            self.load_eng_dict()
        elif mode == Mode.KANA:
            self.load_kana_dict()
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
                print(keyname)
                self.sp.play(keyname)
                self.fontd.change(keyname)

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
