# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 音声素材
# https://amitaro.net/voice/yomiage_01/

from pygame.locals import *
import pygame
import sys
import time
import glob
from threading import Thread
from threading import Timer
from enum import Enum

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


class KeyState(Enum):
    WAIT = 0
    TYPING = 2


class KeyEvent(Enum):
    NOTHING = 0
    CHANGED = 1
    TIMEOUT = 2


class SpellingObserver(Thread):

    def __init__(self):
        super(SpellingObserver,self).__init__()
        self.input_buffer = []
        self.running = True
        self.state = KeyState.WAIT
        self.event = KeyEvent.NOTHING
        return

    def input(self,keyname):
        self.input_buffer += keyname
        print(self.input_buffer)
        self.event = KeyEvent.CHANGED
        print("buffer changed")

    def halt(self):
        self.running = False

    def timerout(self):
        self.event = KeyEvent.TIMEOUT
        print("timeout")

    def matching(self):
        #compare buffer and spell dictionary
        pass

    def report(self):
        #spell was matched and execute special effect
        pass
    def run(self):
        self.timer = None

        while self.running:
            self.curr_len = len(self.input_buffer)

            if self.state == KeyState.WAIT:
                if self.event == KeyEvent.CHANGED:
                    self.state = KeyState.TYPING
                    self.timer = Timer(3, self.timerout)
                    self.timer.start()
                    print("start")
            elif self.state == KeyState.TYPING:
                if self.event == KeyEvent.CHANGED:
                    self.state = KeyState.TYPING
                    if self.matching():
                        self.report()
                        self.input_buffer.clear()
                elif self.event == KeyEvent.TIMEOUT:
                    self.state = KeyState.WAIT
                    self.input_buffer.clear()

            print(f"state={self.state} event={self.event}")
            self.event = KeyEvent.NOTHING

            time.sleep(0.4)


class GameLoop:
    class KeySt(Enum):
        START = 0
        CONTINUE = 1

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

        self.so = SpellingObserver()
        self.so.start()
        return

    def halt_all(self):
        self.so.halt()
        pygame.quit()
        sys.exit()

    def input_key(self) -> str | None:
        keyname = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.halt_all()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.halt_all()
                else:
                    keyname = pygame.key.name(event.key)
        return keyname

    def speak_key(self,keyname):
        #print(keyname)
        if len(keyname) == 1:
            self.so.input(keyname)
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

            if keyname is None:
                pass
            else:
                self.speak_key(keyname)
                fontd = FontDisplay(keyname)

            fontd.draw()
            pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    flags = pygame.FULLSCREEN
    #DISPLAYSURF = pygame.display.set_mode(size=(640,480), display=0, depth=32, flags=pygame.FULLSCREEN)
    DISPLAYSURF = pygame.display.set_mode(size=(640,480), display=0, depth=32)
    pygame.display.set_caption('Hit any key')
    g = GameLoop()
    while True:
        g.do()
        clock.tick(20)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
