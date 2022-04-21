import pygame
from .utils import scale_image
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.Rect, ship_speed, x):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midtop=(x, screen_rect.top))
        self.max_frames_time = (screen_rect.width / ship_speed) * 1.5
        self.frames = 0

    def enemy_hit(self):
        self.frames += 1
        if self.max_frames_time <= self.frames:
            return True
