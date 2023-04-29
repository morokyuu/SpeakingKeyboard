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


def speak_key(keyname, sound):
    print(keyname)
    if len(keyname) == 1:
        val = ord(keyname)
        if 0x61 <= val and val <= 0x7a:
            idx = ord(keyname) - 0x61
            sound[idx].play()
    else:
        return

class AlphabetFont:
    def __init__(self,char="hit any key"):
        self.count = 0
        fontObj = pygame.font.Font('freesansbold.ttf', 100)
        self.charSurfaceObj = fontObj.render(char, True, GREEN, BLUE)
        self.charRectObj = self.charSurfaceObj.get_rect()
        self.charRectObj.center = (300, 300)
    def draw(self):
        DISPLAYSURF.blit(self.charSurfaceObj, self.charRectObj)
        return

def gameLoop():
    fontObj = pygame.font.Font('freesansbold.ttf', 100)
    textSurfaceObj = fontObj.render("Keyboard", True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 150)

    sound_picon = pygame.mixer.Sound('決定ボタンを押す3.mp3')
    sound_picon.play()

    files = glob.glob("./wav/alphabet*.wav")
    files = sorted(files)
    sound_alphabet = [pygame.mixer.Sound(f) for f in files]

    char = AlphabetFont()

    while True:
        DISPLAYSURF.fill(WHITE)
        pygame.draw.polygon(DISPLAYSURF, GREEN,
                            ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
                            )
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

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
                    speak_key(keyname, sound_alphabet)
                    char = AlphabetFont(keyname)

        char.draw()

        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((600, 500), 0, 32)
    pygame.display.set_caption('Hit any key')
    gameLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
