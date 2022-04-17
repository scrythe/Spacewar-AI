import pygame
from utils import scale_image


class Laser(pygame.sprite.Sprite):
    def __init__(self, ship_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/laser.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.rect = self.image.get_rect(midbottom=ship_rect.midtop)
