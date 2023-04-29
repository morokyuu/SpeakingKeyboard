# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import sys

GREEN = (0,255,0)
BLUE = (0,0,123)
WHITE = (255,255,255)


def gameLoop():
    fontObj = pygame.font.Font('freesansbold.ttf',100)
    textSurfaceObj = fontObj.render("Hello",True,GREEN,BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300,150)

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
        pygame.display.update()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((500,400),0,32)
    pygame.display.set_caption('Hit any key')
    gameLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
