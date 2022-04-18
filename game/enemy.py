from time import time
import pygame
from .utils import scale_image
import random


class Enemy(pygame.sprite.Sprite):
    MAX_TIME = 2

    def __init__(self, screen_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.mask = pygame.mask.from_surface(self.image)
        max_left = screen_rect.left+self.image.get_width()
        max_right = screen_rect.right-self.image.get_width()
        random_x = random.randint(max_left, max_right)
        self.rect = self.image.get_rect(midtop=(random_x, screen_rect.top))
        self.start_time = time()

    def enemy_hit(self):
        if self.start_time + self.MAX_TIME <= time():
            return True
