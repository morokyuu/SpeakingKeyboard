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


def input_key(keyname):
    print(keyname)
    if len(keyname) == 1:
        val = ord(keyname)
        if 0x61 <= val and val < 0x7a:
            print("small")

    else:
        return


def gameLoop():
    fontObj = pygame.font.Font('freesansbold.ttf', 100)
    textSurfaceObj = fontObj.render("Hello", True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 150)

    sound_picon = pygame.mixer.Sound('決定ボタンを押す3.mp3')
    sound_picon.play()

    files = glob.glob("./wav/alphabet*.wav")
    files = sorted(files)
    sound_alphabet = [pygame.mixer.Sound(f) for f in files]

    while True:
        DISPLAYSURF.fill(WHITE)
        pygame.draw.polygon(DISPLAYSURF, GREEN,
                            ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))
                            )
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

        #        for s in sound_alphabet:
        #            s.play()
        #            time.sleep(1)
        #            s.stop()

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
                    input_key(keyname)
                    # print(ord(keyname)-0x61)
                    # idx = ord(keyname) - 0x61
                    # sound_alphabet[idx].play()

        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.set_caption('Hit any key')
    gameLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
