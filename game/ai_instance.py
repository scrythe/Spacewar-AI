import neat
import pygame
from .ship import Ship
from .enemy import Enemy
from typing import List


class AI_Instance:
    def __init__(self, genome: neat.DefaultGenome, config, screen_rect: pygame.Rect):
        self.screen_rect = screen_rect
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.player = pygame.sprite.GroupSingle(Ship(self.screen_rect))
        self.player_ship: Ship = self.player.sprite
        self.enemies = pygame.sprite.Group(Enemy(self.screen_rect))
        self.hits = 0

        self.lost = False

    def get_first_enemy(self):
        enemies: List[Enemy] = self.enemies.sprites()
        return enemies[0]

    def run_ai(self):
        self.run_decision()

    def run_decision(self):
        inputs = self.player_ship.ammo, self.player_ship.rect.centerx, self.get_first_enemy().rect.centerx
        output = self.net.activate(inputs)
        decision = output.index(max(output))

        if decision == 0:
            self.player_ship.shoot_laser()
        if decision == 1:
            self.player_ship.move_right()
        if decision == 2:
            self.player_ship.move_left()
        # if 3, then nothing

    def collision(self):
        if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, False, False):
            if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, True, True, pygame.sprite.collide_mask):
                self.hits += 1
                self.player_ship.ammo += 1
                self.enemies.add(Enemy(self.screen_rect))

    def check_lost(self):
        if self.player_ship.ammo == 0 and len(self.player_ship.lasers) == 0:
            self.lost = True

    def update(self):
        self.player.update()
        self.collision()
        self.check_lost()
        if self.get_first_enemy().enemy_hit():
            self.lost = True

    def draw(self, screen):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
