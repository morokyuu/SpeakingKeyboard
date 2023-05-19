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


def english_dict():
    paths = glob.glob("./wav/**/*.mp3",recursive=True)
    names = [os.path.split(f)[1][:-4] for f in paths]
    mp3dict = {name:path for name,path in zip(names,paths)}

    ## rename for symbols
    mp3dict['@'] = "./wav/symbol/at.mp3"
    mp3dict[':'] = "./wav/symbol/colon.mp3"
    mp3dict['.'] = "./wav/symbol/dot.mp3"
    mp3dict[';'] = "./wav/symbol/semicolon.mp3"
    mp3dict['/'] = "./wav/symbol/slash.mp3"
    return mp3dict


def kana_dict():
    paths = glob.glob("./wav/**/*.mp3",recursive=True)
    names = [os.path.split(f)[1][:-4] for f in paths]
    mp3dict = {name:path for name,path in zip(names,paths)}

    with open("hiragana.dat", "r") as fp:
        pairs = [line.rstrip().split(' ') for line in fp.readlines()]
    letter = [p[0] for p in pairs]

    kana_dict = {}
    for p in pairs:
        print(f"--{p}--")
    for p in pairs:
        kana_dict[p[0]] = mp3dict[p[1]]
    # todo ほかにも未割当キーがあるのでKeyError(dictの例外)で落ちる
    # fileを読み込む処理を入れたのなら、直接mp3を指定してもいいような気もする。そのほうが簡単
    # fileの指定を変えるだけで済むから。
    kana_dict['@'] = "./wav/effect/picon.mp3"

    return kana_dict


class SoundPlayer:
    def __init__(self,mp3dict):
        self.dict = mp3dict

    def play(self,name):
        sound = pygame.mixer.Sound(self.dict[name])
        sound.play()




class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        #self.sp = SoundPlayer(english_dict())
        self.sp = SoundPlayer(kana_dict())
        #self.sp.play('picon')

    def change_mode(self):
        self.kana_mode = False
        self.kana_mode = not self.kana_mode
        print(f"change mode {self.kana_mode}")

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
