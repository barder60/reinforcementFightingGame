import pygame
from utils import spritesheet

from constant import background


def StartPygame():
    pygame.init()
    screen = pygame.display.set_mode((895, 860))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, background.get_rect())
        loopVisualBoxer(screen)

    pygame.quit()

    return ''


def loopVisualBoxer(screen):
    blueBoxerImage = pygame.image.load('assets/blue_boxer_sprite.png').convert_alpha()
    sprite_sheet_blue = spritesheet.SpriteSheet(blueBoxerImage)

    redBoxerImage = pygame.image.load('assets/red_boxer_sprite.png').convert_alpha()
    sprite_sheet_red = spritesheet.SpriteSheet(redBoxerImage)

    blueBoxerFrame_0 = sprite_sheet_blue.get_image(6, 115, 205, 1, (0, 0, 0))
    screen.blit(blueBoxerFrame_0, (400, 200))

    redBoxerFrame0 = sprite_sheet_red.get_image(2, 115, 100, 1, (0, 0, 0))
    screen.blit(redBoxerFrame0, (400, 500))
    pygame.display.update()

    blueBoxerFrame_0.set_colorkey((0, 0, 0))
    redBoxerFrame0.set_colorkey((0, 0, 0))

    pygame.display.update()

    blueBoxerFrame1 = sprite_sheet_blue.get_image(4, 115, 100, 1, (0, 0, 0))
    screen.blit(blueBoxerFrame1, (400, 200))

    redBoxerFrame1 = sprite_sheet_red.get_image(4, 115, 100, 1, (0, 0, 0))
    screen.blit(redBoxerFrame1, (400, 500))
    pygame.display.update()

    blueBoxerFrame1.set_colorkey((0, 0, 0))
    redBoxerFrame0.set_colorkey((0, 0, 0))

