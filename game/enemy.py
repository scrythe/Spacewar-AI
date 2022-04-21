import pygame
from .utils import scale_image
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.Rect, ship_speed):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.mask = pygame.mask.from_surface(self.image)
        max_left = screen_rect.left+self.image.get_width()
        max_right = screen_rect.right-self.image.get_width()
        random_x = random.randint(max_left, max_right)
        self.rect = self.image.get_rect(midtop=(random_x, screen_rect.top))
        self.max_frames_time = (screen_rect.width / ship_speed) * 1.2
        self.frames = 0

    def enemy_hit(self):
        self.frames += 1
        if self.max_frames_time <= self.frames:
            return True
