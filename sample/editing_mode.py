import pygame

pygame.init()
screen = pygame.display.set_mode((300,300))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.mod == pygame.KMOD_NONE:
                pass
            elif event.mod & pygame.KMOD_CAPS:
                print("caps----")
        if event.type == pygame.TEXTEDITING:
            print("editing")

    clock.tick(30) # if tick is too slow (ex:1Hz), event not loaded.

pygame.quit()

