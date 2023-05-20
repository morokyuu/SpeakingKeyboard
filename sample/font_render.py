import pygame
#from pygame.locals import *
import sys

def test():
    kana = pygame.image.load("../font/kana_font.png").convert_alpha()
    pygame.draw.circle(screen,(0,0,100),(100,100),50)
    screen.blit(kana,pygame.Rect(0,0,70,70))
    pass

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size=(640,480), display=0, depth=32)
    pygame.display.set_caption('Hit any key')

    while True:
        screen.fill((0,0,0))
        test()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    pygame.quit()