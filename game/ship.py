import pygame
from .utils import scale_image
from .laser import Laser
from time import time


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.Rect):
        super().__init__()
        image = pygame.image.load('assets/spaceship.png').convert_alpha()
        self.image = scale_image(image, 1/4)
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_rect = screen_rect
        self.rect = self.image.get_rect(midbottom=self.screen_rect.midbottom)
        self.lasers = pygame.sprite.Group()
        self.speed = 5
        self.ammo = 8
        self.laser_cooldown = 0.8
        self.last_shot_laser_time = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right >= self.screen_rect.right:
            self.rect.right = self.screen_rect.right

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left <= self.screen_rect.left:
            self.rect.left = self.screen_rect.left

    def shoot_laser(self):
        if self.ammo >= 1 and self.last_shot_laser_time + self.laser_cooldown < time():
            self.lasers.add(Laser(self.rect, self.screen_rect))
            self.ammo -= 1
            return True
        return False

    # def inputs(self, keys):
    #     if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    #         self.move_right()
    #     if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    #         self.move_left()

    def update(self):
        # keys = pygame.key.get_pressed()
        # self.inputs(keys)
        self.lasers.update()
