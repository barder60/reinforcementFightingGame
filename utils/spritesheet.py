import pygame


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, startHeight=0):
        area = ((frame * width), startHeight, width, height)
        image = self.sheet.subsurface(area)
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

