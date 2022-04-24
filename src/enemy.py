import pygame
from utils import scale_image
from random import randint


class Enemy(pygame.sprite.Sprite):
    MAX_SPEED = 2

    def __init__(self, x, screen_rect: pygame.Rect, ship_speed, frames):
        super().__init__()
        image = pygame.image.load('assets/weak-enemy.png')
        self.image = scale_image(image, 1/2)
        self.screen_rect = screen_rect
        self.rect = self.image.get_rect(midtop=(x, self.screen_rect.top))
        self.mask = pygame.mask.from_surface(self.image)
        self.MAX_FRAMES_HIT = (self.screen_rect.width / ship_speed) * 2
        self.MAX_FRAMES_CHANGE_DIRECTION = (
            self.screen_rect.width / ship_speed)
        self.last_shot = frames
        self.last_change_direction = frames
        self.speed = self.MAX_SPEED
        self.enemy_hitted = False

    def move(self):
        self.rect.x += self.speed
        if self.rect.right >= self.screen_rect.right:
            self.rect.right = self.screen_rect.right
        elif self.rect.left <= self.screen_rect.left:
            self.rect.left = self.screen_rect.left

    def update(self, frames):
        self.enemy_hit(frames)
        self.change_direction(frames)
        self.move()

    def change_direction(self, frames):
        if self.last_change_direction + self.MAX_FRAMES_CHANGE_DIRECTION < frames:
            change_direction = randint(0, 1)
            if change_direction:
                self.speed *= -1
                self.last_change_direction = frames

    def enemy_hit(self, frames):
        if self.last_shot + self.MAX_FRAMES_HIT < frames:
            self.last_shot = frames
            self.enemy_hitted = True
