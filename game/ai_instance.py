import neat
import pygame
from .ship import Ship
from .enemy import Enemy
from typing import List


class AI_Instance:
    def __init__(self, genome: neat.DefaultGenome, config, screen_rect: pygame.Rect):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.player = pygame.sprite.GroupSingle(Ship(screen_rect))
        self.player_ship: Ship = self.player.sprite
        self.enemies = pygame.sprite.Group(Enemy(screen_rect))

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

    def update(self):
        self.player.update()

    def draw(self, screen):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
