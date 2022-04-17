import pygame
from utils import scale_image


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/spaceship.png').convert_alpha()
        self.image = scale_image(image, 1/4)
        self.rect = self.image.get_rect(midbottom=screen_rect.midbottom)
