from random import randint
import neat
import pygame
from .ship import Ship
from .enemy import Enemy
from typing import List
from .fitness_function import fitness_function
from time import time


class AI_Instance:
    def __init__(self, genome: neat.DefaultGenome, config, screen_rect: pygame.Rect):
        self.screen_rect = screen_rect
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.player = pygame.sprite.GroupSingle(Ship(self.screen_rect))
        self.player_ship: Ship = self.player.sprite
        self.enemies = pygame.sprite.Group(Enemy(self.screen_rect))
        self.hits = 0
        self.movement_to_player = 0
        self.movement_away_player = 0
        self.bullet_shots = []
        self.frames = 0
        self.near_enemy_counter = 0
        self.shots = 0
        self.start_time = time()

        self.lives = 5

        self.lost = False
        self.color = randint(0, 255), randint(0, 255), randint(0, 255)

    def get_first_enemy(self):
        enemies: List[Enemy] = self.enemies.sprites()
        return enemies[0]

    def run_ai(self):
        self.run_decision()

    def run_decision(self):
        inputs = self.player_ship.ammo, self.player_ship.rect.centerx, self.get_first_enemy(
        ).rect.centerx, len(self.player_ship.lasers)
        shoot, move_direction = self.net.activate(inputs)

        if shoot > 0:
            if self.player_ship.shoot_laser():
                self.bullet_shots.append(
                    self.get_distance_from_enemy())
                self.shots += 1
        if move_direction > 0:
            self.player_ship.move_right()
            if self.player_ship.rect.centerx < self.get_first_enemy().rect.centerx:
                self.movement_to_player += 1
            else:
                self.movement_away_player += 1
        else:
            self.player_ship.move_left()
            if self.player_ship.rect.centerx > self.get_first_enemy().rect.centerx:
                self.movement_to_player += 1
            else:
                self.movement_away_player += 1

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
            self.lives -= 1
            self.enemies.empty()
            self.enemies.add(Enemy(self.screen_rect))
        if self.lives == 0:
            self.lost = True
        self.frames += 1
        self.check_if_near_enemy()

    def check_if_near_enemy(self):
        if self.get_distance_from_enemy() > self.get_first_enemy().rect.width * 1.1:
            self.near_enemy_counter += 1
        else:
            self.near_enemy_counter -= 1

    def get_distance_from_enemy(self):
        distance_diffrence = self.player_ship.rect.centerx - \
            self.get_first_enemy().rect.centerx
        return abs(distance_diffrence)

    def draw_line(self, screen: pygame.Surface):
        start_pos = self.player_ship.rect.midtop
        end_pos = self.get_first_enemy().rect.midbottom
        pygame.draw.line(screen, self.color, start_pos, end_pos)

    def evaluate(self):
        fitness = fitness_function(
            self.frames, self.movement_to_player, self.movement_away_player, self.screen_rect.width, self.bullet_shots, self.hits, self.shots, self.start_time)

        self.genome.fitness = fitness

    def draw(self, screen):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.draw_line(screen)
