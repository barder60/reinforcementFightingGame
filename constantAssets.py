import pygame

from utils import spritesheet

# ASSETS
background = pygame.image.load("assets/ring_de_box.PNG")

redBoxerImage = pygame.image.load('assets/red_boxer_sprite.png').convert_alpha()
sprite_sheet_red = spritesheet.SpriteSheet(redBoxerImage)

blueBoxerImage = pygame.image.load('assets/blue_boxer_sprite.png').convert_alpha()
sprite_sheet_blue = spritesheet.SpriteSheet(blueBoxerImage)

# RED_BOXER

RED_PUNCH_DOING = sprite_sheet_red.get_image(5, 92, 100, 1)

RED_PUNCH_LEFT_START = sprite_sheet_red.get_image(2, 70, 100, 1)
RED_PUNCH_LEFT_DONE = sprite_sheet_red.get_image(5, 93, 100, 1, 100)

RED_PUNCH_RIGHT_START = sprite_sheet_red.get_image(0, 93, 100, 1)
RED_PUNCH_RIGHT_DONE = sprite_sheet_red.get_image(0, 93, 100, 1, 90)

RED_BASIC_MOVEMENT_LEFT = sprite_sheet_red.get_image(3, 80, 100, 1)
RED_BASIC_MOVEMENT_RIGHT = sprite_sheet_red.get_image(4, 90, 100, 1)


RED_KO_START = sprite_sheet_red.get_image(1, 110, 100, 1, 100)
RED_KO_DOING = sprite_sheet_red.get_image(2, 110, 120, 1, 100)
RED_KO_DONE = sprite_sheet_red.get_image(3, 115, 120, 1, 100)

# BLUE_BOXER

BLUE_PUNCH_LEFT_START = sprite_sheet_red.get_image(2, 70, 100, 1)
BLUE_PUNCH_LEFT_DONE = sprite_sheet_red.get_image(5, 93, 100, 1, 100)

BLUE_PUNCH_DOING = sprite_sheet_blue.get_image(5, 93, 100, 1, 132)

BLUE_BASIC_MOVEMENT_LEFT = sprite_sheet_blue.get_image(3, 80, 100, 1, 132)
BLUE_BASIC_MOVEMENT_RIGHT = sprite_sheet_blue.get_image(5, 80, 100, 1, 132)

BLUE_PUNCH_RIGHT_START = sprite_sheet_blue.get_image(0, 90, 100, 1, 132)
BLUE_PUNCH_RIGHT_DONE = sprite_sheet_blue.get_image(5, 93, 130, 1)


BLUE_KO_START = sprite_sheet_blue.get_image(1, 115, 100, 1)
BLUE_KO_DOING = sprite_sheet_blue.get_image(2, 115, 120, 1)
BLUE_KO_DONE = sprite_sheet_blue.get_image(3, 115, 120, 1)