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

clock = pygame.time.Clock()

def speak_key(keyname, sound):
    #print(keyname)
    if len(keyname) == 1:
        if keyname.islower():
            idx = ord(keyname) - 0x61
            sound[idx].play()
    else:
        return

class AlphabetFont:
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
        return

    def input_key(self) -> str | None:
        keyname = None
        for event in pygame.event.get():
            if event.type == pygame.TEXTEDITING:
                #if enter this mode, next key event will be treated as ESC to exit text-editing mode.
                print("text-editing")

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_NONE:
                    pass
                else:
                    if event.mod & pygame.KMOD_CAPS:
                        ## https://www.pygame.org/docs/ref/key.html#pygame.key.name
                        print("capslock")

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    keyname = pygame.key.name(event.key)
        return keyname
    def do(self):
        char = AlphabetFont()
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
                print(f"{keyname} len={len(keyname)}")

            if keyname is None:
                pass
            else:
                speak_key(keyname, self.sound_alphabet)
                char = AlphabetFont(keyname)

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
        clock.tick(60)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
