import pygame
from utils import scale_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, screen_rect: pygame.Rect, ship_speed):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png')
        self.image = scale_image(image, 1/2)
        self.rect = self.image.get_rect(midtop=(x, screen_rect.top))
        self.mask = pygame.mask.from_surface(self.image)
        self.MAX_FRAMES = (screen_rect.width / ship_speed) * 1.25
        self.last_shot = 0

    def enemy_hit(self, frames):
        if self.last_shot + self.MAX_FRAMES < frames:
            self.last_shot = frames
            return True
