import pygame
from .utils import scale_image
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.mask = pygame.mask.from_surface(self.image)
        random_x = random.randrange(screen_rect.left, screen_rect.right)
        self.rect = self.image.get_rect(midtop=(random_x, screen_rect.top))
