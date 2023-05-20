import pygame
#from pygame.locals import *
import sys

def test():
    kana = pygame.image.load("../font/kana_font.png").convert_alpha()
    for i in range(5):
        screen.blit(kana,(30+i*80,70),pygame.Rect(0,i*70+8,70,70))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size=(640,480), display=0, depth=32)
    pygame.display.set_caption('Hit any key')

    for n,i in enumerate([1,3,4]):
        print(f"{n} {i}")

    while True:
        screen.fill((0,0,0))
        test()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    pygame.quit()

