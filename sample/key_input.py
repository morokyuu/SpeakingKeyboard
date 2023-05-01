import pygame

pygame.init()
screen = pygame.display.set_mode((300,300))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(event)
            if event.key == pygame.K_a:
                print("hello")
    clock.tick(30) # if tick is too slow (ex:1Hz), event not loaded.

pygame.quit()

