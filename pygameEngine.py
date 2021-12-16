import pygame

from utils import spritesheet

pygame.init()
screen = pygame.display.set_mode((895, 860))

from constantAssets import background, RED_BASIC_MOVEMENT_LEFT, RED_BASIC_MOVEMENT_RIGHT, BLUE_BASIC_MOVEMENT_LEFT, \
    BLUE_BASIC_MOVEMENT_RIGHT, RED_PUNCH_LEFT_START, RED_PUNCH_LEFT_DONE, RED_PUNCH_DOING, RED_PUNCH_RIGHT_DONE, \
    RED_PUNCH_RIGHT_START, RED_KO_START, RED_KO_DOING, RED_KO_DONE, BLUE_PUNCH_RIGHT_DONE, BLUE_PUNCH_RIGHT_START, \
    BLUE_PUNCH_DOING, BLUE_KO_DONE, BLUE_KO_DOING, BLUE_KO_START

RED_ANIMATIONS = [
    RED_BASIC_MOVEMENT_RIGHT,
    RED_BASIC_MOVEMENT_LEFT
]

clock = pygame.time.Clock()
lastUpdated = pygame.time.get_ticks()


def StartPygame():
    running = True
    screen.blit(background, background.get_rect())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)



        loopVisualBoxer(screen)
        pygame.display.update()
    pygame.quit()
    return ''


def loopVisualBoxer(screen):
    return ''
    # screen.blit(actionDuPlayer, (posX, posY))




