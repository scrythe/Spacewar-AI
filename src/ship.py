import pygame
from utils import scale_image
from laser import Laser


def create_rect(image: pygame.Surface, screen_rect: pygame.Rect):
    rect = image.get_rect()
    rect.midbottom = screen_rect.midbottom
    return rect


class Ship(pygame.sprite.Sprite):
    SPEED = 5
    MAX_AMMO = 2
    SHOT_DELAY = 250

    def __init__(self, screen_rect: pygame.Rect, x):
        super().__init__()
        image = pygame.image.load('assets/spaceship.png').convert_alpha()
        self.image = scale_image(image, 1/4)
        self.screen_rect = screen_rect
        self.rect = create_rect(self.image, self.screen_rect)

        self.lasers = pygame.sprite.Group()
        self.ammo = self.MAX_AMMO
        self.last_shot = 0

    def move_right(self):
        self.rect.x += self.SPEED
        if self.rect.right >= self.screen_rect.right:
            self.rect.right = self.screen_rect.right

    def move_left(self):
        self.rect.x -= self.SPEED
        if self.rect.left <= self.screen_rect.left:
            self.rect.left = self.screen_rect.left

    def check_able_shoot(self, frames):
        enoug_ammo = self.ammo >= 1
        not_exceeded_time = self.last_shot + self.SHOT_DELAY < frames
        return enoug_ammo and not_exceeded_time

    def shoot_laser(self, frames):
        if self.check_able_shoot(frames):
            self.lasers.add(Laser(self.rect, self.screen_rect))
            self.last_shot = frames
            self.ammo -= 1
            return True
        return False

    def update(self):
        self.lasers.update()
