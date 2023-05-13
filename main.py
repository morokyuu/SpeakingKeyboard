# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pygame.locals import *
import pygame
import sys
import time
import glob

GREEN = (0, 255, 0)
BLUE = (0, 0, 123)
WHITE = (255, 255, 255)



class FontDisplay:
    def __init__(self,char="hit any key"):
        fontObj = pygame.font.Font('freesansbold.ttf', 130)
        if len(char)==1:
            if char.islower():
                char = char.upper()
            char = " " + char + " "
        self.charSurfaceObj = fontObj.render(char, True, GREEN, BLUE)
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


class GameLoop:
    def __init__(self):
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        self.textSurfaceObj = fontObj.render("Speaking Keyboard", True, GREEN, BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (300, 150)

        self.sound_picon = pygame.mixer.Sound('決定ボタンを押す3.mp3')
        self.sound_picon.play()

        files = glob.glob("./wav/alphabet*.wav")
        files = sorted(files)
        self.sound_alphabet = [pygame.mixer.Sound(f) for f in files]

        files = glob.glob("./wav/number/*.mp3")
        files = sorted(files)
        self.sound_number = [pygame.mixer.Sound(f) for f in files]

        files = {'.':"dot.mp3",';':"semicolon.mp3",'/':"slash.mp3",':':"colon.mp3",'@':"at.mp3"}
        self.sound_symbol = {f:pygame.mixer.Sound("./wav/symbol/"+files[f]) for f in files.keys()}
        return

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
                idx = ord(keyname) - 0x61
                self.sound_alphabet[idx].play()
            elif keyname.isdigit():
                idx = int(keyname)
                self.sound_number[idx].play()
            elif keyname in '.;:@/':
                self.sound_symbol[keyname].play()
        else:
            return

    def do(self):
        char = FontDisplay()
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

            if keyname is None:
                pass
            else:
                self.speak_key(keyname)
                char = FontDisplay(keyname)

            char.draw()
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
