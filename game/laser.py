import pygame
from .utils import scale_image


class Laser(pygame.sprite.Sprite):
    def __init__(self, ship_rect: pygame.Rect, screen_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/laser.png').convert_alpha()
        self.image = scale_image(image, 1/2)
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_rect = screen_rect
        self.rect = self.image.get_rect(midbottom=ship_rect.midtop)
        self.speed = 10

    def move_top(self):
        self.rect.y -= self.speed

    def check_top(self):
        if self.rect.bottom <= self.screen_rect.top:
            self.kill()

    def update(self):
        self.move_top()
        self.check_top()
