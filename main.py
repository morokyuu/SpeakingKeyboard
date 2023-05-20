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

GREEN = (0, 255, 0)
BLUE = (0, 0, 123)
WHITE = (255, 255, 255)



class FontDisplay:
    def __init__(self,char="hit any key"):
        fontObj = pygame.font.Font('freesansbold.ttf', 130)

        self.char = char
        if len(self.char)==1:
            if self.char.islower():
                self.char = self.char.upper()
            self.char = " " + self.char + " "
        self.charSurfaceObj = fontObj.render(self.char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)

    def draw(self):
        DISPLAYSURF.blit(self.charSurfaceObj, self.charRectObj)
        return


class State:
    def __init__(self):
        return

    def transition(self):
        return

class KanaDict:
    def __init__(self):
        with open("hiragana.dat", "r") as fp:
            self.pairs = [line.rstrip().split(' ') for line in fp.readlines()]
        self.letter = [p[0] for p in self.pairs]

    def get(self,key_name):
        assert key_name in self.letter, "not for kana-moji key"
        return self.pairs[key_name]


class SoundPlayer:
    def __init__(self):
        with open("eng_mode","r") as fp:
            lines = [line.rstrip() for line in fp.readlines()]

        self.mp3dict = {}
        for line in lines:
            col = line.split(' ')
            assert len(col) == 3,"file: num of column error."
            self.mp3dict[col[0]] = col[2]

        self.mp3dict["picon"] = "./wav/effect/picon.mp3"

    def play(self,name):
        path = self.mp3dict[name]
        if len(path) > 1:
            sound = pygame.mixer.Sound(path)
            sound.play()


class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        self.sp = SoundPlayer()
        self.sp.play('picon')

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

    def speak_key(self,keyname):
        #print(keyname)
        if len(keyname) == 1:
            if keyname.islower():
                assert keyname in string.ascii_lowercase, "not ascii_lowercase"
                self.sp.play(keyname)
            elif keyname.isdigit():
                assert keyname in string.digits, "not digits"
                self.sp.play(keyname)
            elif keyname in '.;:@/':
                assert keyname in string.punctuation, "not punctuation"
                self.sp.play(keyname)
        else:
            return

    def do(self):
        fontd = FontDisplay()
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
                self.speak_key(keyname)
                fontd = FontDisplay(keyname)

            fontd.draw()
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
